import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict) -> str:
    """Generate a JWT token."""
    payload = data.copy()
    payload.update({"exp": datetime.timestamp(datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Verify a JWT token and return its payload."""
    try:
        print(f"Token: {token}")
        print(f"Secret Key: {SECRET_KEY}")
        print(f"Algorithm: {ALGORITHM}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
