from fastapi import APIRouter, HTTPException
from app.models import Category, Product
from app.database import SessionLocal

router = APIRouter()


@router.get("/")
async def read_categories():
    db = SessionLocal()
    categories = db.query(Category).all()
    db.close()
    return categories


@router.get("/{category_id}")
async def read_category(category_id: int):
    db = SessionLocal()
    category = db.query(Category).filter(Category.category_id == category_id).first()
    db.close()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/")
async def create_category(name: str, description: str):
    db = SessionLocal()
    category = Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.close()
    return {"msg": "Category created successfully"}

# count of categories
@router.get("/count")
async def count_categories():
    db = SessionLocal()
    count = db.query(Category).count()
    db.close()
    return {"count": count}

# count of products
@router.get("/{category_id}/products/count")
async def count_products(category_id: int):
    db = SessionLocal()
    count = db.query(Product).filter(Product.category_id == category_id).count()
    db.close()
    return {"count": count}


@router.put("/{category_id}")
async def update_category(category_id: int, name: str, description: str):
    db = SessionLocal()
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = name
    category.description = description
    db.commit()
    db.close()
    return {"msg": "Category updated successfully"}

@router.delete("/{category_id}")
async def delete_category(category_id: int):
    db = SessionLocal()
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    db.close()
    return {"msg": "Category deleted successfully"}

# get N of product 
@router.get("/{category_id}/products")
async def get_products_by_category(category_id: int):
    db = SessionLocal()
    products = db.query(Product).filter(Product.category_id == category_id).all()
    db.close()
    return products

@router.get("/{category_id}/products/{product_id}")
async def get_product_by_category(category_id: int, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/{category_id}/products")
async def create_product(category_id: int, name: str, description: str, price: float, stock_quantity: int):
    db = SessionLocal()
    product = Product(name=name, description=description, price=price, stock_quantity=stock_quantity, category_id=category_id)
    db.add(product)
    db.commit()
    db.close()
    return {"msg": "Product created successfully"}

@router.put("/{category_id}/products/{product_id}")
async def update_product(category_id: int, product_id: int, name: str, description: str, price: float, stock_quantity: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = name
    product.description = description
    product.price = price
    product.stock_quantity = stock_quantity
    db.commit()
    db.close()
    return {"msg": "Product updated successfully"}

@router.delete("/{category_id}/products/{product_id}")
async def delete_product(category_id: int, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    db.close()
    return {"msg": "Product deleted successfully"}

