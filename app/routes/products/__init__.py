from fastapi import APIRouter, HTTPException, Depends
from app.models import Product, Category, Order, OrderDetail, User
from app.database import SessionLocal

router = APIRouter()

@router.get("/")
async def read_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

# count of products
@router.get("/count")
async def count_products():
    db = SessionLocal()
    count = db.query(Product).count()
    db.close()
    return {"count" : count}

@router.get("/{product_id}")
async def read_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# product cat

@router.post("/")
async def create_product(name: str, description: str, price: float, category_id: int):
    db = SessionLocal()
    product = Product(name=name, description=description, price=price, category_id=category_id)
    db.add(product)
    db.commit()
    db.close()
    return {"msg": "Product created successfully"}

@router.put("/{product_id}")
async def update_product(product_id: int, name: str, description: str, price: float, category_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = name
    product.description = description
    product.price = price
    product.category_id = category_id
    db.commit()
    db.close()
    return {"msg": "Product updated successfully"}

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    db.close()
    return {"msg": "Product deleted successfully"}

@router.get("/{product_id}/category")
async def read_product_category(product_id: int):
    db = SessionLocal()
    category = db.query(Category).join(Product).filter(Product.product_id == product_id).first()
    db.close()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{product_id}/orders")
async def read_product_orders(product_id: int):
    db = SessionLocal()
    orders = db.query(Order).join(OrderDetail).filter(OrderDetail.product_id == product_id).all()
    db.close()
    return orders

@router.get("/{product_id}/orders/{order_id}")
async def read_product_order(product_id: int, order_id: int):
    db = SessionLocal()
    order = db.query(Order).join(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/{product_id}/orders/{order_id}/details")
async def read_product_order_details(product_id: int, order_id: int):
    db = SessionLocal()
    order_details = db.query(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id).all()
    db.close()
    return order_details

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}")
async def read_product_order_detail(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    order_detail = db.query(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    db.close()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return order_detail

@router.get("/orders/{order_id}/user")
async def read_product_order_user(order_id: int):
    db = SessionLocal()
    user = db.query(User).join(Order).filter(Order.id == order_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/order")
async def read_product_order_detail_order(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    order = db.query(Order).join(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/order/user")
async def read_product_order_detail_order_user(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    user = db.query(User).join(Order).join(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/product/order")
async def read_product_order_detail_product_order(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    order = db.query(Order).join(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/product/order/user")
async def read_product_order_detail_product_order_user(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    user = db.query(User).join(Order).join(OrderDetail).join(Product).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/product")
async def read_product_order_detail_product(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    product = db.query(Product).join(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/product/category")
async def read_product_order_detail_product_category(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    category = db.query(Category).join(Product).join(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).first()
    db.close()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/product/category/products")
async def read_product_order_detail_product_category_products(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    products = db.query(Product).join(Category).join(OrderDetail).filter(OrderDetail.product_id == product_id, OrderDetail.order_id == order_id, OrderDetail.id == order_detail_id).all()
    db.close()
    return products
