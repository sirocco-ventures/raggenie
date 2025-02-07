import requests
from app.schemas.common import LoginData
import os
from fastapi import APIRouter, Response, Depends, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from app.providers.config import configs
from app.utils.jwt import JWTUtils
from app.schemas.common import CommonResponse
from app.providers.middleware import verify_token
from typing import Optional
from app.providers.config import configs

login = APIRouter()


# @login.post("/login")
# def login_user(response: Response, user: LoginData):
#     if user.username == configs.username and user.password == configs.password:
#         jwt_utils = JWTUtils(configs.secret_key)
#         token = jwt_utils.create_jwt_token(data={"sub": user.username})

#         return CommonResponse(
#             status=True,
#             status_code=200,
#             message="Login Successful",
#             data={"token": token},
#             error=None
#         )
#     else:
#         return CommonResponse(
#             status=False,
#             status_code=401,
#             message="Invalid credentials",
#             data=None,
#             error=None,
#         )



@login.post("/login")
def login_user(response: Response, user: LoginData):
    if not user.username or not user.password:
        return {
            "status": False,
            "status_code": 401,
            "message": "Invalid credentials",
            "data": None,
            "error": None,
        }

    try:
        response = requests.post(
            f"{configs.zitadel_domain}/v2/sessions",
            json={"checks": {"user": {"loginName": user.username}}},
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            },
        )
        
        response.raise_for_status()
        session_data = response.json()
        session_id = session_data.get("sessionId")
        #add condition to check sessionId
        sessionToken = session_data.get("sessionToken")
        validate_response = requests.patch(
            f"{configs.zitadel_domain}/v2/sessions/{session_id}",
            json={"checks": {"password": {"password": user.password}}},
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            },
        )
        
        validate_response.raise_for_status()
        validated_session_data = validate_response.json()
        
        return {
            "session_data" : validated_session_data,
            "session_id" : session_id
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to create session", "details": str(e)}, 500
    
# will redirect to idp when called with ipdId
# need to set successurl and failureUrl dynamically *****
@login.get("/login/idp/{idp_id}")
def idp_login(response: Response, idp_id : int):
    # print(idp_id)
    try:
        response = requests.post(
            f"{configs.zitadel_domain}/v2/idp_intents",
            json={
                "idpId": f"{idp_id}",
                "urls": {
                    "successUrl": "http://0.0.0.0:8001/api/v1/auth/idp/success",
                    "failureUrl": "https://google.com"
                }
            },
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            })
        response.raise_for_status()
        auth_url = response.json().get('authUrl',"")
        
        
        if auth_url:
            return RedirectResponse(url=auth_url)  # Redirect to auth_url
        
        return {"error": "authUrl not found"}, 400
        
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to retrieve idp auth url", "details": str(e)}, 500

# if idp login is success then is redirected to this endpoint with which we get the user
# details from the idp (currently only tested with google) need to send the userdata to front-end
@login.get("/idp/success")
def idp_success(request: Request):
    query_params = request.query_params
    # print(query_params)
    idp_intent_id = query_params.get("id")
    token = query_params.get("token")
    user_id = query_params.get("user","")
    try:
        response = requests.post(
            f"{configs.zitadel_domain}/v2/idp_intents/{int(idp_intent_id)}",
            json={"idpIntentToken": token},
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            },
        )
        
        response.raise_for_status()
        user_data = response.json()
        # print(user_data)
        if(user_id):
            session_response = create_user_session(user_id, idp_intent_id, token)
            return {
                "login_response": session_response
            }
        else:
            create_user_response = create_user(user_data, idp_intent_id, token)
            return create_user_response
        
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to create session", "details": str(e)}, 500


#  Helper function to create a user session
def create_user_session(user_id: str, idp_intent_id: str, token: str):

    login_response = requests.post(
        f"{configs.zitadel_domain}/v2/sessions",
        json={
            "checks": {
                "user": {
                    "userId": user_id
                },
                "idpIntent": {
                    "idpIntentId": idp_intent_id,
                    "idpIntentToken": token
                }
            }
        },
        headers={
            "Authorization": f"Bearer {configs.zitadel_cctoken}",
            "Content-Type": "application/json",
        }
    )
    return login_response.json()

# Helper function to create a user and their session
def create_user(user_data: dict, idp_intent_id: str, token: str):
    
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
            "email": "aanshaad09@gmail.com",
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
    
    create_user_response = requests.post(
        f"{configs.zitadel_domain}/v2/users/human",
        json=payload,
        headers={
            "Authorization": f"Bearer {configs.zitadel_cctoken}",
            "Content-Type": "application/json",
        }
    )
    
    create_user_response.raise_for_status()
    created_user_data = create_user_response.json()
    user_id = created_user_data.get("userId")
    if not user_id:
        return {
            "status": "error",
            "message": "error while creating user",
        }, 500
    
    # need to add error handling when user created and failed to create session +++
    # Create session for the newly created user
    session_response = create_user_session(
        created_user_data.get("userId"),
        idp_intent_id,
        token
    )
    
    return {
        "status": "success", 
        "user_data": created_user_data,
        "session_data": session_response
    }
    
# endpoint to retreive all the available idp providers that is setup in Zitadel
@login.get("/idp/list")
def list_idp(response: Response):
    
    try: 
        response = requests.post(
            f"{configs.zitadel_domain}/management/v1/idps/templates/_search",
            json={
                "query": {
                    "offset": "0",
                    "limit": 100,
                    "asc": True
                }
            },
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            },
            )
        response.raise_for_status()
        idp_data = response.json()
        idp_list = [{"id" : item.get('id'), "type" : item.get('type')} for item in idp_data.get('result', [])]
        
        return {
            "idp_list" : idp_list
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to retrieve identity provider info", "details": str(e)}, 500


# need to change this
@login.get("/userdetails/{session_id}")
def get_user(request: Request, response: Response, session_id : int):

    try:
        response = requests.get(
            f"{configs.zitadel_domain}/v2/sessions/{session_id}",
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            },
        )
        
        response.raise_for_status()
        session_data = response.json()
        
        return {
            "session_data" : session_data
        }

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to validate session", "details": str(e)}, 500
    






@login.get("/user_info", dependencies=[Depends(verify_token)])
def get_user_info(request: Request, sub: Optional[str] = Depends(verify_token)):
    if sub is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not authenticated"
    )

    return CommonResponse(
        status=True,
        status_code=200,
        message="User info retrieved successfully",
        data={ "username": sub, "auth_enabled": configs.auth_enabled },
        error=None
    )
    
    
@login.post("/logout",dependencies=[Depends(verify_token)])
def logout_user(response: Response):
    return CommonResponse(
        status=True,
        status_code=200,
        message="Logout Successful",
        data=None,
        error=None
    )