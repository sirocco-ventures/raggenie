from datetime import datetime, timezone
import json
from app.providers.zitadel import Zitadel
import requests
from app.utils.jwt import JWTUtils
from app.providers.config import configs
from fastapi import Request, status, HTTPException, Cookie
from fastapi import Request, HTTPException, status
from typing import Optional

zitadel = Zitadel()

async def verify_token(request: Request, session_data: Optional[str] = Cookie(None)):

    if configs.auth_enabled:

        try:
            session_data = json.loads(session_data)  # This handles None and invalid JSON
            session_id = session_data.get("session_id")
            session_token = session_data.get("session_token")
            user_id = session_data.get("user_id")


            
            if not session_id or not session_token:
                raise ValueError("missing session data")
            response = zitadel.get_user_info(session_id)
            session_expiry = response.get("session").get("expirationDate")
            session_expiry_utc = datetime.fromisoformat(session_expiry.rstrip("Z")).replace(tzinfo=timezone.utc)
            now_utc = datetime.now(timezone.utc)
            if (session_expiry_utc - now_utc).total_seconds() < 300:
                zitadel.refresh_session(session_id)
            
        except (TypeError, json.JSONDecodeError, AttributeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing session data"
            )
        
        except requests.exceptions.RequestException as e:  # Handles request errors (e.g., network issues, 404)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Session validation failed: {str(e)}",
            )
        return {"session_id": session_id, "user_id": user_id}
    else:
        return configs.default_username

