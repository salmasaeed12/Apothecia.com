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

@router.get("/{order_id}/details")
async def read_order_details(order_id: int, db: Session = Depends(get_db)):
    order_details = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()
    return order_details

@router.get("/{order_id}/details/{order_detail_id}")
async def read_order_detail(order_id: int, order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return order_detail

@router.post("/{order_id}/details")
async def create_order_detail(order_id: int, product_id: int, quantity: int, price: float, db: Session = Depends(get_db)):
    order_detail = OrderDetail(order_id=order_id, product_id=product_id, quantity=quantity, price=price)
    db.add(order_detail)
    db.commit()
    return {"msg": "Order detail created successfully"}

@router.put("/{order_id}/details/{order_detail_id}")
async def update_order_detail(order_id: int, order_detail_id: int, product_id: int, quantity: int, price: float, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    order_detail.product_id = product_id
    order_detail.quantity = quantity
    order_detail.price = price
    db.commit()
    return {"msg": "Order detail updated successfully"}

@router.delete("/{order_id}/details/{order_detail_id}")
async def delete_order_detail(order_id: int, order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    db.delete(order_detail)
    db.commit()
    return {"msg": "Order detail deleted successfully"}

@router.get("/{order_id}/details/{order_detail_id}/product")
async def read_order_detail_product(order_id: int, order_detail_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).join(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{order_id}/user")
async def read_order_user(order_id: int, db: Session = Depends(get_db)):
    user = db.query(User).join(Order).filter(Order.id == order_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{order_id}/details/{order_detail_id}/order")
async def read_order_detail_order(order_id: int, order_detail_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).join(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/{order_id}/details/{order_detail_id}/order/user")
async def read_order_detail_order_user(order_id: int, order_detail_id: int, db: Session = Depends(get_db)):
    user = db.query(User).join(Order).join(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{order_id}/details/{order_detail_id}/product/order")
async def read_order_detail_product_order(order_id: int, order_detail_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).join(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/{order_id}/details/{order_detail_id}/product/order/user")
async def read_order_detail_product_order_user(order_id: int, order_detail_id: int, db: Session = Depends(get_db)):
    user = db.query(User).join(Order).join(OrderDetail).join(Product).filter(OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
