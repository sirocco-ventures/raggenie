from app.utils.jwt import JWTUtils
from app.providers.config import configs
from fastapi import Request, status, HTTPException


from fastapi import Request, HTTPException, status
from typing import Optional

async def verify_token(request: Request) -> Optional[str]:
    jwt_utils = JWTUtils(configs.secret_key)

    if configs.auth_enabled:
        auth_header = request.headers.get("Authorization")
        token = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):]

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
