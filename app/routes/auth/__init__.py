from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate
from app.models import User
from werkzeug.security import generate_password_hash

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    existing_user = await User.filter(email=user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = generate_password_hash(user.password)
    new_user = await User.create(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed_password
    )

    return {"msg": "User created successfully"}

