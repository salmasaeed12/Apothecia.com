from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Supplier 
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
async def read_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return suppliers

# Count of suppliers
@router.get("/count")
async def count_suppliers(db: Session = Depends(get_db)):
    count = db.query(Supplier).count()
    return {"count": count}

@router.get("/{supplier_id}")
async def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.post("/")
async def create_supplier(name: str, contact_person: str, phone: str, email: str, address: str, db: Session = Depends(get_db)):
    supplier = Supplier(name=name, contact_person=contact_person, phone=phone, email=email, address=address)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return {"msg": "Supplier created successfully"}

@router.put("/{supplier_id}")
async def update_supplier(supplier_id: int, name: str, contact_person: str, phone: str, email: str, address: str, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier.name = name
    supplier.contact_person = contact_person
    supplier.phone = phone
    supplier.email = email
    supplier.address = address
    db.commit()
    return {"msg": "Supplier updated successfully"}

@router.delete("/{supplier_id}")
async def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()
    return {"msg": "Supplier deleted successfully"}

@router.get("/search")
async def search_supplier(name: str, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.name == name).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.get("/{supplier_id}/products")
async def read_supplier_products(supplier_id: int, db: Session = Depends(get_db)):
    supplier_products = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).all()
    return supplier_products

@router.get("/{supplier_id}/products/{product_id}")
async def read_supplier_product(supplier_id: int, product_id: int, db: Session = Depends(get_db)):
    supplier_product = db.query(Supplier).filter(Supplier.supplier_id == supplier_id, Supplier.product_id == product_id).first()
    if supplier_product is None:
        raise HTTPException(status_code=404, detail="Supplier product not found")
    return supplier_product

@router.post("/{supplier_id}/products")
async def create_supplier_product(supplier_id: int, product_id: int, db: Session = Depends(get_db)):
    supplier_product = Supplier(supplier_id=supplier_id, product_id=product_id)
    db.add(supplier_product)
    db.commit()
    return {"msg": "Supplier product created successfully"}

@router.delete("/{supplier_id}/products/{product_id}")
async def delete_supplier_product(supplier_id: int, product_id: int, db: Session = Depends(get_db)):
    supplier_product = db.query(Supplier).filter(Supplier.supplier_id == supplier_id, Supplier.product_id == product_id).first()
    if supplier_product is None:
        raise HTTPException(status_code=404, detail="Supplier product not found")
    db.delete(supplier_product)
    db.commit()
    return {"msg": "Supplier product deleted successfully"}

@router.get("/{supplier_id}/orders")
async def read_supplier_orders(supplier_id: int, db: Session = Depends(get_db)):
    supplier_orders = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).all()
    return supplier_orders

@router.get("/{supplier_id}/orders/{order_id}")
async def read_supplier_order(supplier_id: int, order_id: int, db: Session = Depends(get_db)):
    supplier_order = db.query(Supplier).filter(Supplier.supplier_id == supplier_id, Supplier.order_id == order_id).first()
    if supplier_order is None:
        raise HTTPException(status_code=404, detail="Supplier order not found")
    return supplier_order

@router.post("/{supplier_id}/orders")
async def create_supplier_order(supplier_id: int, order_id: int, db: Session = Depends(get_db)):
    supplier_order = Supplier(supplier_id=supplier_id, order_id=order_id)
    db.add(supplier_order)
    db.commit()
    return {"msg": "Supplier order created successfully"}