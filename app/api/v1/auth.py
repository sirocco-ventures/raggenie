from app.schemas.common import LoginData
import os
from fastapi import APIRouter, Response, HTTPException, status
from app.utils.authlogin import AuthMiddleware
from app.providers.config import configs

login = APIRouter()


@login.post("/")
def login_user(response: Response, user: LoginData):
    if user.username == configs.username and user.password == configs.password:
        auth =  AuthMiddleware(configs.secret_key, "HS256", "auth_token", configs.auth_server)
        token = auth.create_access_token(data={"sub": user.username})
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            max_age=3600,
            path="/",
            domain=configs.auth_server
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