import os
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Request, status
import app.schemas.common as resp_schemas
from fastapi.responses import JSONResponse
from app.providers.config import configs



class AuthMiddleware:
    def __init__(self):
        self.SECRET_KEY = configs.SECRET_KEY
        self.ALGORITHM = "HS256"
        self.COOKIE_NAME = "auth_token"
        self.AUTH_SERVER = configs.AUTH_SERVER

        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is missing from environment variables")

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=30)):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

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

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username = payload.get("sub")
            if username is None:
                return resp_schemas.CommonResponse(
                    status=False,
                    status_code=401,
                    message="Invalid token",
                    data={},
                    error="Username missing from token"
                )
        except PyJWTError:
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

        new_token = self.create_access_token(data={"sub": username})
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
