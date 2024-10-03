
import app.schemas.common as resp_schemas
from app.schemas.common import LoginData
import os
from fastapi import APIRouter, Response, HTTPException, status
from app.utils.authlogin import AuthMiddleware


AUTH_SERVER = os.getenv("AUTH_SERVER")


login = APIRouter()


@login.post("/")
def login_user(response: Response, user: LoginData):
    print(user.username, user.password)
    print(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    if user.username == os.getenv("USERNAME") and user.password == os.getenv("PASSWORD"):
        auth =  AuthMiddleware()
        token = auth.create_access_token(data={"sub": user.username})
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            max_age=3600,
            path="/",
            domain=AUTH_SERVER
        )
        return {
            "status": True,
            "status_code": 200,
            "message": "Login Successful",
            "data": {"token": token},
            "error": None
        }
    else:
        return {
            "status": False,
            "status_code": 401,
            "message": "Invalid credentials",
            "data": {"token": {}},
            "error": "Invalid credentials"
        }

def is_error_response(message:str, err:str, data:dict):
    return resp_schemas.CommonResponse(
            status= False,
            status_code=422,
            message=message,
            data=data,
            error=err
        )

def is_none_reponse(message:str, data:dict):
    return resp_schemas.CommonResponse(
            status= True,
            status_code=200,
            message=message,
            data=data,
            error="Not Found"
        )