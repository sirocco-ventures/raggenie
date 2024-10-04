import os
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Request, status
import app.schemas.common as resp_schemas
from fastapi.responses import JSONResponse
from app.providers.config import configs



from app.utils.jwt import JWTUtils

class AuthMiddleware:
    def __init__(self, secret_key, algorithm, cookie_name, auth_server):
        self.jwt_utils = JWTUtils(secret_key, algorithm)
        self.COOKIE_NAME = cookie_name
        self.AUTH_SERVER = auth_server

        if not secret_key:
            raise ValueError("SECRET_KEY is missing from environment variables")

    async def __call__(self, request: Request, call_next):
        if request.url.path.startswith("/api/v1/login/") or request.url.path.startswith("/api/v1/query/") or request.url.path in ["/docs", "/docs#", "/openapi.json", "/redoc"]:
            return await call_next(request)

        token = request.cookies.get(self.COOKIE_NAME)

        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=resp_schemas.CommonResponse(
                    status=False,
                    status_code=401,
                    message="Authentication required",
                    data={},
                    error="Authentication required"
                ).model_dump()
            )

        payload = self.jwt_utils.decode_jwt_token(token)
        if payload is None or "sub" not in payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=resp_schemas.CommonResponse(
                    status=False,
                    status_code=401,
                    message="Invalid token",
                    data={},
                    error="Token decoding failed"
                ).model_dump()
            )

        username = payload["sub"]
        new_token = self.jwt_utils.create_jwt_token(data={"sub": username})
        response = await call_next(request)
        response.set_cookie(
            key=self.COOKIE_NAME,
            value=new_token,
            httponly=True,
            max_age=3600,
            path="/",
            domain=self.AUTH_SERVER
        )
        return response

