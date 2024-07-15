from fastapi import APIRouter, HTTPException, Depends
from app.models import User
from app.database import SessionLocal
from app.auth import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/register")
async def register(first_name: str, last_name: str, email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        raise HTTPException(status_code=400, detail="email already exists")

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.add(new_user)
    db.commit()
    db.close()

    return {"msg": "User created successfully"}

@router.post("/login")
async def login(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email")
    
    if  not check_password_hash(user.password_hash, password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.user_id, "email": current_user.email}
