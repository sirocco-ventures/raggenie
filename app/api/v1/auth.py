from app.schemas.common import LoginData
import os
from fastapi import APIRouter, Response, Depends, Request, Response, HTTPException, status
from app.providers.config import configs
from app.utils.jwt import JWTUtils
from app.schemas.common import CommonResponse
from app.providers.middleware import verify_token
from typing import Optional

login = APIRouter()


@login.post("/login")
def login_user(response: Response, user: LoginData):
    if user.username == configs.username and user.password == configs.password:
        jwt_utils = JWTUtils(configs.secret_key)
        token = jwt_utils.create_jwt_token(data={"sub": user.username})

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
        data={"username": sub},
        error=None
    )