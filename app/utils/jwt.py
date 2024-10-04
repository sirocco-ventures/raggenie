import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Request, status
import app.schemas.common as resp_schemas
from fastapi.responses import JSONResponse
from app.providers.config import configs

class JWTUtils:
    def __init__(self, secret_key, algorithm):
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=30)):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except PyJWTError:
            return None
