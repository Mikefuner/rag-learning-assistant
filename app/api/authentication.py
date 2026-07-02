from dotenv import load_dotenv
from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import hmac, os

load_dotenv()

API_KEY = os.getenv("API_TOKEN")

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not hmac.compare_digest(token, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )