from fastapi import APIRouter, HTTPException, Depends
from app.models import User
from app.database import SessionLocal
from app.auth import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.dependencies import get_current_user
from app.models.Order import Order

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

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    db.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/users")
async def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@router.put("/users/{user_id}")
async def update_user(user_id: int, first_name: str, last_name: str, email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    db.commit()
    db.close()
    return {"msg": "User updated successfully"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    db.close()
    return {"msg": "User deleted successfully"}

@router.get("/users/count")
async def count_users():
    db = SessionLocal()
    count = db.query(User).count()
    db.close()
    return {"count": count}

@router.get("/users/{user_id}/orders")
async def user_orders(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    orders = user.orders
    db.close()
    return orders
#i dont know the proplem here
@router.get("/users/{user_id}/orders/count")
async def count_user_orders(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    count = user.orders.count()
    db.close()
    return {"count": count}

@router.get("/users/{user_id}/orders/{order_id}")
async def user_order(user_id: int, order_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    order = user.orders.filter(Order.id == order_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/users/{user_id}/orders/{order_id}/products")
async def user_order_products(user_id: int, order_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    order = user.orders.filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    products = order.products
    db.close()
    return products