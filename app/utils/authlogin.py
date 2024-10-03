import os
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
import app.schemas.common as resp_schemas
from fastapi.responses import JSONResponse


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
COOKIE_NAME = "auth_token"
AUTH_SERVER = os.getenv("AUTH_SERVER")

class AuthMiddleware:
    def __init__(self):
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY is missing from environment variables")

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=30)):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def __call__(self, request: Request, call_next):
        if request.url.path.startswith("/api/v1/login/") or request.url.path.startswith("/api/v1/query/") or request.url.path in ["/docs", "/docs#", "/openapi.json", "/redoc"]:
            return await call_next(request)

        token = request.cookies.get(COOKIE_NAME)

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
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
            key=COOKIE_NAME,
            value=new_token,
            httponly=True,
            max_age=3600,
            path="/",
            domain=AUTH_SERVER
        )
        return response
