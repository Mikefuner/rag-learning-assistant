from dotenv import load_dotenv
from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import hmac, os
from security.rate_limiter import RateLimiter

load_dotenv()

API_KEY = os.getenv("API_TOKEN")

security = HTTPBearer()
rate_limiter = RateLimiter()

async def verify_access(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if not hmac.compare_digest(token, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    if not rate_limiter.allow(token):
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )