from datetime import datetime, timezone
import json

import requests
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
            
            if not session_id or not session_token:
                raise ValueError("missing session data")
            response = requests.get(
                f"{configs.zitadel_domain}/v2/sessions/{session_id}",
                headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
                }
            )
            response.raise_for_status()
            session_expiry = response.json().get("session").get("expirationDate")
            session_expiry_utc = datetime.fromisoformat(session_expiry.rstrip("Z")).replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > session_expiry_utc:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
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
        
        return session_id
    else:
        return configs.default_username

