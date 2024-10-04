import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Request, status, HTTPException
from app.providers.config import configs

class JWTUtils:
    def __init__(self, secret_key, algorithm):
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm

    def create_jwt_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=30)):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_jwt_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except PyJWTError:
            return None


jwt_utils = JWTUtils(configs.secret_key, "HS256")

async def verify_token(request: Request):
    if configs.auth_enabled:
        token = request.cookies.get("auth_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        payload = jwt_utils.decode_jwt_token(token)
        if payload is None or "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return payload["sub"]
    else:
        return None
