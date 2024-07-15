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
