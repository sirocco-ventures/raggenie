from app.schemas.common import LoginData
import os
from fastapi import APIRouter, Response, HTTPException, status
from app.utils.authlogin import AuthMiddleware
from app.providers.config import configs

login = APIRouter()


@login.post("/")
def login_user(response: Response, user: LoginData):
    print(user.username, user.password)
    print(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    if user.username == configs.USERNAME and user.password == configs.PASSWORD:
        auth =  AuthMiddleware()
        token = auth.create_access_token(data={"sub": user.username})
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            max_age=3600,
            path="/",
            domain=configs.AUTH_SERVER
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