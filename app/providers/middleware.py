from app.utils.jwt import JWTUtils
from app.providers.config import configs
from fastapi import Request, status, HTTPException

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