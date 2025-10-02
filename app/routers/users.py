from fastapi import APIRouter, BackgroundTasks, Depends

from app.schemas import UserCreate
from app.security import get_password_hash
from app.dependencies import get_current_user, get_db


router = APIRouter(prefix="/users", tags=["users"])


def send_welcome_email(email: str):
    print(f"Sending welcome email to {email}")


@router.post("/register")
async def register_user(user: UserCreate, background_tasks: BackgroundTasks):
    user_data = user.dict()
    if user_data.get("password"):
        user_data["password"] = get_password_hash(user_data["password"])  # hash password
    new_user = {"id": 1, **user_data}
    background_tasks.add_task(send_welcome_email, user.email)
    return {"message": "User registered successfully", "user": new_user}


@router.get("/me/items")
async def read_own_items(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
):
    return [
        {"item_id": 1, "owner": current_user["username"]},
        {"item_id": 2, "owner": current_user["username"]},
    ]


