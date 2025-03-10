import json
import requests
import time
import app.schemas.user as schemas
import app.repository.user as repo
from app.providers.config import configs
from app.schemas.common import CommonResponse
from fastapi.responses import JSONResponse, RedirectResponse
from jwt import encode


class Zitadel:
    
    def __init__(self):
        self.base_url = configs.zitadel_domain
        with open(configs.client_private_key_file_path, "r") as f:
            json_data = json.load(f)
        self.private_key = json_data["key"]
        self.kid = json_data["keyId"]
        self.user_id = json_data["userId"]
        self.token = None  # Will store the access token
        self.token_expiry = 0  # Timestamp when token expires
        self._refresh_token()  # Generate initial token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        
        
    def _generate_jwt(self):
        """Generate a signed JWT."""
        header = {"alg": "RS256", "kid": self.kid}
        payload = {
            "iss": self.user_id,
            "sub": self.user_id,
            "aud": configs.zitadel_domain,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600  # 1-hour expiry
        }
        return encode(payload, self.private_key, algorithm="RS256", headers=header)
    
    def _refresh_token(self):
        """Fetch a new OAuth access token using the JWT."""
        jwt_token = self._generate_jwt()
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "scope": f"openid email profile urn:zitadel:iam:org:project:id:zitadel:aud",
            "assertion": jwt_token
        }
        response = requests.post(configs.zitadel_token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
            self.token_expiry = int(time.time()) + 3500
        else:
            raise Exception(f"Failed to fetch access token: {response.text}")
        
        
    def _ensure_valid_token(self):
        """Ensure the token is valid, refreshing if expired."""
        if time.time() >= self.token_expiry:
            self._refresh_token()
        self.headers["Authorization"] = f"Bearer {self.token}"
        
    
    def create_user_session(self , user_id: str, idp_intent_id: str, token: str):
        """ create session for a user and sets the session cookie."""
        self._ensure_valid_token()
        try:
            response = requests.post(
                f"{self.base_url}/v2/sessions",
                json={
                    "checks": {
                        "user": {
                            "userId": user_id
                        },
                        "idpIntent": {
                            "idpIntentId": idp_intent_id,
                            "idpIntentToken": token
                        }
                    },
                    "lifetime": "1800.000000000s"
                },
                headers=self.headers
            )
            response.raise_for_status()
            
            session_data = response.json()
            session_id = session_data.get("sessionId")
            session_token = session_data.get("sessionToken")
            
            if not session_id or not session_token:
                return JSONResponse(
                    status_code=500,
                    content={"error": "Session ID or token not found in response"}
                )
                
            json_response = JSONResponse(
                status_code=201,
                content={"message": "Session created successfully", "session_id": session_id, "user_id": user_id},
            )
            json_response.set_cookie(
                key="session_data",
                value=json.dumps({"session_id": session_id, "session_token": session_token, "user_id": user_id}),
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=1800,
                path="/",
            )

            return json_response
        
        except requests.RequestException as e:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Failed to create session",
                    "details": str(e)
                }
            )
                
    
    def create_user(self, user_data: dict, idp_intent_id: str, token: str):
        """ Create a user from IDP authentication data """
        # ONLY WORKS WITH GOOGLE IDP AUTHENTICATION DATA NOW NEED TO MAKE MODIFICATION
        self._ensure_valid_token()      
        idp_info = user_data.get("idpInformation", {})
        raw_info = idp_info.get("rawInformation", {})
        user_info = raw_info.get("User", {})
        
        payload = {
            "username": user_info.get("email", ""),
            "profile": {
                "givenName": user_info.get("given_name", ""),
                "familyName": user_info.get("family_name", ""),
                "displayName": user_info.get("name", "")
            },
            "email": {
                "email":  user_info.get("email", ""),
                "isVerified": user_info.get("email_verified", False),
            },
            "idpLinks": [
                {
                    "idpId": idp_info.get("idpId"),
                    "userId": idp_info.get("userId"),
                    "userName": user_info.get("name", "")
                }
            ],
        }
        try:
            response = requests.post(
                f"{self.base_url}/v2/users/human", json=payload, headers=self.headers
            )
            response.raise_for_status()

            created_user_data = response.json()
            user_id = created_user_data.get("userId")

            if not user_id:
                return JSONResponse(
                    status_code=500, content={"error": "User creation failed"}
                )
                
            return self.create_user_session(user_id, idp_intent_id, token)

        except requests.RequestException as e:
            return JSONResponse(
                status_code=500, content={"error": "Failed to create user", "details": str(e)}
            )
    
    def redirect_to_idp(self, idp_id: int):
        """ Generate an authentication url for idp login and redirect user to the url """
        # need to set successurl and failureUrl domain dynamically *****
        self._ensure_valid_token()
        try:
            response = requests.post(
                f"{self.base_url}/v2/idp_intents",
                json={
                    "idpId": f"{idp_id}",
                    "urls": {
                        "successUrl": "http://0.0.0.0:8001/api/v1/auth/idp/success",
                        "failureUrl": "http://0.0.0.0:8001/ui/login"
                }
                },
                headers=self.headers
            )
            response.raise_for_status()
            auth_url = response.json().get('authUrl')
            
            if auth_url:
                return RedirectResponse(url=auth_url)
            
            return JSONResponse(status_code=400, content={"error": "authUrl not found"})
            
        except requests.exceptions.RequestException as e:
            return JSONResponse(
                status_code=500, content={"error": "Failed to retrieve IDP auth URL", "details": str(e)}
            )
    
    def get_user_info(self, session_id: int):
        """ get user info from the current session """
        # need to add error handling when there is no userinfo retreived from the 
        # session 
        self._ensure_valid_token()
        try:
            response = requests.get(
                f"{self.base_url}/v2/sessions/{session_id}",
                headers=self.headers
            )
            response.raise_for_status()
            session_info = response.json()
            return session_info
        except requests.exceptions.RequestException as e:
               return CommonResponse(
                status=False,
                status_code=500,
                message="User info retrieval failed",
                data=None,
                error=str(e),
            )
        
    def get_idp_intent_data(self,idp_intent_id: int, idp_token: str):
        self._ensure_valid_token()
        try:
            response = requests.post(
                f"{self.base_url}/v2/idp_intents/{idp_intent_id}",
                json={"idpIntentToken": idp_token},
                headers=self.headers
            )  
            response.raise_for_status()
            return response
        
        except requests.exceptions.RequestException as e:
            return JSONResponse(
                status_code=500, content={"error": "Failed to fetch user data with idp_intend_id", "details": str(e)}
            )
        
    def list_idp_providers(self):
        self._ensure_valid_token()
        try: 
            response = requests.post(
                f"{self.base_url}/management/v1/idps/templates/_search",
                json={
                    "query": {
                        "offset": "0",
                        "limit": 100,
                        "asc": True
                    }
                },
                headers=self.headers
                )
            response.raise_for_status()
            idp_data = response.json()
            idp_list = [{"id" : item.get('id'), "type" : item.get('type')} for item in idp_data.get('result', [])]
            
            return {
                "idp_list" : idp_list
            }
        
        except requests.exceptions.RequestException as e:
            return {"error": "Failed to retrieve identity provider info", "details": str(e)}, 500
        
    
    def logout_user(self, session_id: str):
        """Logout user by deleting the session."""
        self._ensure_valid_token()
        try:
            response = requests.delete(
                f"{self.base_url}/v2/sessions/{session_id}",
                headers=self.headers,
            )
            response.raise_for_status()

            return CommonResponse(
                status=True,
                status_code=response.status_code,
                message="Logout Successful" if response.status_code == 200 else "Logout Unsuccessful",
                data=response.json(),
                error=None,
            )

        except requests.RequestException as e:
            return CommonResponse(
                status=False,
                status_code=500,
                message="Logout Failed",
                data=None,
                error=str(e),
            )