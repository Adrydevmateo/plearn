from fastapi import APIRouter, HTTPException, status
from typing import Optional
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
async def login(user_id: Optional[str] = None):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is required")

    token = create_access_token(data={"user_id": user_id})
    return {"access_token": token, "token_type": "bearer"}
