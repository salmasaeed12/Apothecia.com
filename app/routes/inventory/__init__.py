from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Inventory
from app.database import SessionLocal
from datetime import datetime

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def read_inventory(db: Session = Depends(get_db)):
    inventory = db.query(Inventory).all()
    return inventory

# Count of inventory entries
@router.get("/count")
async def count_inventory(db: Session = Depends(get_db)):
    count = db.query(Inventory).count()
    return {"count": count}

@router.get("/{inventory_id}")
async def read_inventory_entry(inventory_id: int, db: Session = Depends(get_db)):
    inventory_entry = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory_entry is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    return inventory_entry

@router.post("/")
async def create_inventory_entry(product_id: int, supplier_id: int, quantity: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory_entry = Inventory(product_id=product_id, supplier_id=supplier_id, quantity=quantity, received_date=received_date)
    db.add(inventory_entry)
    db.commit()
    db.refresh(inventory_entry)
    return {"msg": "Inventory entry created successfully"}

@router.put("/{inventory_id}")
async def update_inventory_entry(inventory_id: int, product_id: int, supplier_id: int, quantity: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory_entry = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory_entry is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    inventory_entry.product_id = product_id
    inventory_entry.supplier_id = supplier_id
    inventory_entry.quantity = quantity
    inventory_entry.received_date = received_date
    db.commit()
    return {"msg": "Inventory entry updated successfully"}

@router.delete("/{inventory_id}")
async def delete_inventory_entry(inventory_id: int, db: Session = Depends(get_db)):
    inventory_entry = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory_entry is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    db.delete(inventory_entry)
    db.commit()
    return {"msg": "Inventory entry deleted successfully"}
