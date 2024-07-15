from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Order, OrderDetail, Product, User
from app.database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def read_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

# Count of orders
@router.get("/count")
async def count_orders(db: Session = Depends(get_db)):
    count = db.query(Order).count()
    return {"count": count}

@router.get("/{order_id}")
async def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/")
async def create_order(user_id: int, product_id: int, quantity: int, total_price: float, db: Session = Depends(get_db)):
    order = Order(user_id=user_id, total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)
    
    order_detail = OrderDetail(order_id=order.id, product_id=product_id, quantity=quantity, price=total_price)
    db.add(order_detail)
    db.commit()
    
    return {"msg": "Order created successfully"}

@router.put("/{order_id}")
async def update_order(order_id: int, user_id: int, total_price: float, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order.user_id = user_id
    order.total_price = total_price
    db.commit()
    return {"msg": "Order updated successfully"}

@router.delete("/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"msg": "Order deleted successfully"}
