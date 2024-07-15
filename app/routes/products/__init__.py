from fastapi import APIRouter, HTTPException, Depends
from app.models import Product
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


