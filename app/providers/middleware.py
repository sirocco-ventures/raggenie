import json
from app.utils.jwt import JWTUtils
from app.providers.config import configs
from fastapi import Request, status, HTTPException, Cookie
from fastapi import Request, HTTPException, status
from typing import Optional

async def verify_token(request: Request, session_data: Optional[str] = Cookie(None)):
    # jwt_utils = JWTUtils(configs.secret_key)

        # auth_header = request.headers.get("Authorization")
        # token = None
    if configs.auth_enabled:

        try:
            session_data = json.loads(session_data)  # This handles None and invalid JSON
            session_id = session_data.get("session_id")
            session_token = session_data.get("session_token")
        except (TypeError, json.JSONDecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing session data"
            )

        # print(session_id, session_token)

        if not session_id or not session_token:
            print("trigger")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        return session_id
    else:
        return configs.default_username


        # if auth_header and auth_header.startswith("Bearer "):
        #     token = auth_header[len("Bearer "):]

        # if not token:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Authentication required"
        #     )

        # payload = jwt_utils.decode_jwt_token(token)
        # if payload is None or "sub" not in payload:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Invalid token"
        #     )

        # return payload["sub"]
    # else:
    #     return configs.default_username
