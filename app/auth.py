from fastapi import HTTPException, security
from fastapi.security import APIKeyCookie

from app.config import API_KEY

api_key_header = APIKeyCookie(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key"
        )
    return api_key