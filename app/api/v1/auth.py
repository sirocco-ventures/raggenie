from app.schemas.common import LoginData
import os
from fastapi import APIRouter, Response
from app.providers.config import configs
from app.utils.jwt import JWTUtils
from app.schemas.common import CommonResponse

login = APIRouter()


@login.post("/")
def login_user(response: Response, user: LoginData):
    if user.username == configs.username and user.password == configs.password:
        jwt_utils = JWTUtils(configs.secret_key)
        token = jwt_utils.create_jwt_token(data={"sub": user.username})
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            max_age=3600,
            path="/",
            domain=configs.auth_server
        )
        return CommonResponse(
            status=True,
            status_code=200,
            message="Login Successful",
            data={"token": token},
            error=None
        )
    else:
        return CommonResponse(
            status=False,
            status_code=401,
            message="Invalid credentials",
            data=None,
            error=None,
        )