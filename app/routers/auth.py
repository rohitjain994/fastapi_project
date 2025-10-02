from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="", tags=["auth"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data.username:
        raise HTTPException(status_code=400, detail="Username required")
    return {
        "access_token": f"dummy-token-for-{form_data.username}",
        "token_type": "bearer",
    }


