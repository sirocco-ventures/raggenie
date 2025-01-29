from requests import post,get
from fastapi.responses import  RedirectResponse
from fastapi import APIRouter, Response, Depends, Request, Response, HTTPException, status
from app.providers.config import configs
from app.schemas.common import CommonResponse
from app.providers.middleware import verify_token
from app.providers.config import configs
from oauthlib.oauth2 import WebApplicationClient
from fastapi.security import HTTPBearer
from fastapi import HTTPException,status
login = APIRouter()
http_bearer = HTTPBearer()


 



@login.get("/login")
def login_user(response: Response,response_class=RedirectResponse):
    client = WebApplicationClient(configs.cclient_id)
    authorization_url = configs.cauthorization_url
    url = client.prepare_request_uri(
        authorization_url,
        redirect_uri = configs.credirect_url ,
        scope = ['openid','email'],
        # state = 'D8VAo311AAl_49LAtM51HA'
    )
    print(url)
    return RedirectResponse(url, status_code=301)

 



@login.get('/callback')
def callback_route(request: Request, response_class=RedirectResponse):
    code = request.query_params.get('code')
    # print(code)
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing authorization code"
        )

    token_url = configs.ctoken_url
    client = WebApplicationClient(configs.cclient_id)
    token_request_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': configs.credirect_url,
        'client_id': configs.cclient_id,
        'client_secret': configs.cclient_secret
    }

    response = post(token_url, data=token_request_data)

    if response.ok:
        token_data = response.json()
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        
        print(access_token)
        response = RedirectResponse(url=f"http://localhost:5000/auth?access_token={access_token}")
        response.set_cookie("access_token", access_token, httponly=True, secure=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to exchange authorization code"
        )



@login.get('/userinfo')
async def userinfo(user_data:dict=Depends(verify_token)):
    return {"message":"Token is Valid","user_details":user_data}
    




@login.post("/logout",dependencies=[Depends(verify_token)])
def logout_user(response: Response):
    return CommonResponse(
        status=True,
        status_code=200,
        message="Logout Successful",
        data=None,
        error=None
    )

@login.get("/user_info", dependencies=[Depends(verify_token)])
def get_user_info(request: Request, sub:str = Depends(verify_token)):
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