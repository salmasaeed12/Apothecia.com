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

@router.delete("/")
async def delete_all_inventory_entries(db: Session = Depends(get_db)):
    db.query(Inventory).delete()
    db.commit()
    return {"msg": "All inventory entries deleted successfully"}

@router.get("/product/{product_id}")
async def read_inventory_by_product(product_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).all()
    return inventory

@router.get("/supplier/{supplier_id}")
async def read_inventory_by_supplier(supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/received/{received_date}")
async def read_inventory_by_received_date(received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date).all()
    return inventory

@router.get("/quantity/{quantity}")
async def read_inventory_by_quantity(quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.quantity == quantity).all()
    return inventory

@router.get("/quantity/less/{quantity}")
async def read_inventory_by_quantity_less(quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.quantity < quantity).all()
    return inventory

@router.get("/quantity/more/{quantity}")
async def read_inventory_by_quantity_more(quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.quantity > quantity).all()
    return inventory

@router.get("/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_quantity_between(quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/received/before/{received_date}")
async def read_inventory_received_before(received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date < received_date).all()
    return inventory

@router.get("/received/after/{received_date}")
async def read_inventory_received_after(received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date > received_date).all()
    return inventory

@router.get("/received/between/{received_date1}/{received_date2}")
async def read_inventory_received_between(received_date1: datetime, received_date2: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date.between(received_date1, received_date2)).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}")
async def read_inventory_by_product_supplier(product_id: int, supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}")
async def read_inventory_by_product_received(product_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date).all()
    return inventory

@router.get("/product/{product_id}/quantity/{quantity}")
async def read_inventory_by_product_quantity(product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.quantity == quantity).all()
    return inventory

@router.get("/product/{product_id}/quantity/less/{quantity}")
async def read_inventory_by_product_quantity_less(product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.quantity < quantity).all()
    return inventory

@router.get("/product/{product_id}/quantity/more/{quantity}")
async def read_inventory_by_product_quantity_more(product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.quantity > quantity).all()
    return inventory

@router.get("/product/{product_id}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_product_quantity_between(product_id: int, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/received/before/{received_date}")
async def read_inventory_by_product_received_before(product_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date < received_date).all()
    return inventory

@router.get("/product/{product_id}/received/after/{received_date}")
async def read_inventory_by_product_received_after(product_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date > received_date).all()
    return inventory

@router.get("/product/{product_id}/received/between/{received_date1}/{received_date2}")
async def read_inventory_by_product_received_between(product_id: int, received_date1: datetime, received_date2: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date.between(received_date1, received_date2)).all()
    return inventory

@router.get("/supplier/{supplier_id}/received/{received_date}")
async def read_inventory_by_supplier_received(supplier_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.received_date == received_date).all()
    return inventory

@router.get("/supplier/{supplier_id}/quantity/{quantity}")
async def read_inventory_by_supplier_quantity(supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.quantity == quantity).all()
    return inventory

@router.get("/supplier/{supplier_id}/quantity/less/{quantity}")
async def read_inventory_by_supplier_quantity_less(supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.quantity < quantity).all()
    return inventory

@router.get("/supplier/{supplier_id}/quantity/more/{quantity}")
async def read_inventory_by_supplier_quantity_more(supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.quantity > quantity).all()
    return inventory

@router.get("/supplier/{supplier_id}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_supplier_quantity_between(supplier_id: int, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/supplier/{supplier_id}/received/before/{received_date}")
async def read_inventory_by_supplier_received_before(supplier_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.received_date < received_date).all()
    return inventory

@router.get("/supplier/{supplier_id}/received/after/{received_date}")
async def read_inventory_by_supplier_received_after(supplier_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.received_date > received_date).all()
    return inventory

@router.get("/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}")
async def read_inventory_by_supplier_received_between(supplier_id: int, received_date1: datetime, received_date2: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2)).all()
    return inventory

@router.get("/received/{received_date}/quantity/{quantity}")
async def read_inventory_by_received_quantity(received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.quantity == quantity).all()
    return inventory

@router.get("/received/{received_date}/quantity/less/{quantity}")
async def read_inventory_by_received_quantity_less(received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.quantity < quantity).all()
    return inventory

@router.get("/received/{received_date}/quantity/more/{quantity}")
async def read_inventory_by_received_quantity_more(received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.quantity > quantity).all()
    return inventory

@router.get("/received/{received_date}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_received_quantity_between(received_date: datetime, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/received/{received_date}/product/{product_id}")
async def read_inventory_by_received_product(received_date: datetime, product_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.product_id == product_id).all()
    return inventory

@router.get("/received/{received_date}/supplier/{supplier_id}")
async def read_inventory_by_received_supplier(received_date: datetime, supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/received/{received_date}/product/{product_id}/supplier/{supplier_id}")
async def read_inventory_by_received_product_supplier(received_date: datetime, product_id: int, supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.product_id == product_id, Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/received/{received_date}/product/{product_id}/quantity/{quantity}")
async def read_inventory_by_received_product_quantity(received_date: datetime, product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.product_id == product_id, Inventory.quantity == quantity).all()
    return inventory

@router.get("/received/{received_date}/product/{product_id}/quantity/less/{quantity}")
async def read_inventory_by_received_product_quantity_less(received_date: datetime, product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.product_id == product_id, Inventory.quantity < quantity).all()
    return inventory

@router.get("/received/{received_date}/product/{product_id}/quantity/more/{quantity}")
async def read_inventory_by_received_product_quantity_more(received_date: datetime, product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.product_id == product_id, Inventory.quantity > quantity).all()
    return inventory

@router.get("/received/{received_date}/product/{product_id}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_received_product_quantity_between(received_date: datetime, product_id: int, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.product_id == product_id, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/received/{received_date}/supplier/{supplier_id}/quantity/{quantity}")
async def read_inventory_by_received_supplier_quantity(received_date: datetime, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity == quantity).all()
    return inventory

@router.get("/received/{received_date}/supplier/{supplier_id}/quantity/less/{quantity}")
async def read_inventory_by_received_supplier_quantity_less(received_date: datetime, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity < quantity).all()
    return inventory

@router.get("/received/{received_date}/supplier/{supplier_id}/quantity/more/{quantity}")
async def read_inventory_by_received_supplier_quantity_more(received_date: datetime, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity > quantity).all()
    return inventory

@router.get("/received/{received_date}/supplier/{supplier_id}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_received_supplier_quantity_between(received_date: datetime, supplier_id: int, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/{quantity}")
async def read_inventory_by_product_supplier_quantity(product_id: int, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity == quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/less/{quantity}")
async def read_inventory_by_product_supplier_quantity_less(product_id: int, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity < quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/more/{quantity}")
async def read_inventory_by_product_supplier_quantity_more(product_id: int, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity > quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_product_supplier_quantity_between(product_id: int, supplier_id: int, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/{received_date}")
async def read_inventory_by_product_supplier_received(product_id: int, supplier_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date == received_date).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/before/{received_date}")
async def read_inventory_by_product_supplier_received_before(product_id: int, supplier_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date < received_date).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/after/{received_date}")
async def read_inventory_by_product_supplier_received_after(product_id: int, supplier_id: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}")
async def read_inventory_by_product_supplier_received_between(product_id: int, supplier_id: int, received_date1: datetime, received_date2: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2)).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/{quantity}/received/{received_date}")
async def read_inventory_by_product_supplier_quantity_received(product_id: int, supplier_id: int, quantity: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity == quantity, Inventory.received_date == received_date).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/less/{quantity}/received/{received_date}")
async def read_inventory_by_product_supplier_quantity_less_received(product_id: int, supplier_id: int, quantity: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity < quantity, Inventory.received_date == received_date).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/more/{quantity}/received/{received_date}")
async def read_inventory_by_product_supplier_quantity_more_received(product_id: int, supplier_id: int, quantity: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity > quantity, Inventory.received_date == received_date).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/quantity/between/{quantity1}/{quantity2}/received/{received_date}")
async def read_inventory_by_product_supplier_quantity_between_received(product_id: int, supplier_id: int, quantity1: int, quantity2: int, received_date: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.quantity.between(quantity1, quantity2), Inventory.received_date == received_date).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/before/{received_date}/quantity/{quantity}")
async def read_inventory_by_product_supplier_received_before_quantity(product_id: int, supplier_id: int, received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date < received_date, Inventory.quantity == quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/after/{received_date}/quantity/{quantity}")
async def read_inventory_by_product_supplier_received_after_quantity(product_id: int, supplier_id: int, received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date, Inventory.quantity == quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}/quantity/{quantity}")
async def read_inventory_by_product_supplier_received_between_quantity(product_id: int, supplier_id: int, received_date1: datetime, received_date2: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2), Inventory.quantity == quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/before/{received_date}/quantity/less/{quantity}")
async def read_inventory_by_product_supplier_received_before_quantity_less(product_id: int, supplier_id: int, received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date < received_date, Inventory.quantity < quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/after/{received_date}/quantity/less/{quantity}")
async def read_inventory_by_product_supplier_received_after_quantity_less(product_id: int, supplier_id: int, received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date, Inventory.quantity < quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}/quantity/less/{quantity}")
async def read_inventory_by_product_supplier_received_between_quantity_less(product_id: int, supplier_id: int, received_date1: datetime, received_date2: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2), Inventory.quantity < quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/before/{received_date}/quantity/more/{quantity}")
async def read_inventory_by_product_supplier_received_before_quantity_more(product_id: int, supplier_id: int, received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date < received_date, Inventory.quantity > quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/after/{received_date}/quantity/more/{quantity}")
async def read_inventory_by_product_supplier_received_after_quantity_more(product_id: int, supplier_id: int, received_date: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date, Inventory.quantity > quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}/quantity/more/{quantity}")
async def read_inventory_by_product_supplier_received_between_quantity_more(product_id: int, supplier_id: int, received_date1: datetime, received_date2: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2), Inventory.quantity > quantity).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/before/{received_date}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_product_supplier_received_before_quantity_between(product_id: int, supplier_id: int, received_date: datetime, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date < received_date, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/after/{received_date}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_product_supplier_received_after_quantity_between(product_id: int, supplier_id: int, received_date: datetime, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_product_supplier_received_between_quantity_between(product_id: int, supplier_id: int, received_date1: datetime, received_date2: datetime, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2), Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/quantity/{quantity}/supplier/{supplier_id}")
async def read_inventory_by_product_received_quantity_supplier(product_id: int, received_date: datetime, quantity: int, supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.quantity == quantity, Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/quantity/less/{quantity}/supplier/{supplier_id}")
async def read_inventory_by_product_received_quantity_less_supplier(product_id: int, received_date: datetime, quantity: int, supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.quantity < quantity, Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/quantity/more/{quantity}/supplier/{supplier_id}")
async def read_inventory_by_product_received_quantity_more_supplier(product_id: int, received_date: datetime, quantity: int, supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.quantity > quantity, Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/quantity/between/{quantity1}/{quantity2}/supplier/{supplier_id}")
async def read_inventory_by_product_received_quantity_between_supplier(product_id: int, received_date: datetime, quantity1: int, quantity2: int, supplier_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.quantity.between(quantity1, quantity2), Inventory.supplier_id == supplier_id).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/{quantity}")
async def read_inventory_by_product_received_supplier_quantity(product_id: int, received_date: datetime, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity == quantity).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/less/{quantity}")
async def read_inventory_by_product_received_supplier_quantity_less(product_id: int, received_date: datetime, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity < quantity).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/more/{quantity}")
async def read_inventory_by_product_received_supplier_quantity_more(product_id: int, received_date: datetime, supplier_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity > quantity).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_product_received_supplier_quantity_between(product_id: int, received_date: datetime, supplier_id: int, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/before/{received_date1}")
async def read_inventory_by_product_received_supplier_received_before(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date < received_date1).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/after/{received_date1}")
async def read_inventory_by_product_received_supplier_received_after(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date1).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}")
async def read_inventory_by_product_received_supplier_received_between(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, received_date2: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2)).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/{quantity}/received/before/{received_date1}")
async def read_inventory_by_product_received_supplier_quantity_received_before(product_id: int, received_date: datetime, supplier_id: int, quantity: int, received_date1: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity == quantity, Inventory.received_date < received_date1).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/less/{quantity}/received/before/{received_date1}")
async def read_inventory_by_product_received_supplier_quantity_less_received_before(product_id: int, received_date: datetime, supplier_id: int, quantity: int, received_date1: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity < quantity, Inventory.received_date < received_date1).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/more/{quantity}/received/before/{received_date1}")
async def read_inventory_by_product_received_supplier_quantity_more_received_before(product_id: int, received_date: datetime, supplier_id: int, quantity: int, received_date1: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity > quantity, Inventory.received_date < received_date1).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/quantity/between/{quantity1}/{quantity2}/received/before/{received_date1}")
async def read_inventory_by_product_received_supplier_quantity_between_received_before(product_id: int, received_date: datetime, supplier_id: int, quantity1: int, quantity2: int, received_date1: datetime, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.quantity.between(quantity1, quantity2), Inventory.received_date < received_date1).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/after/{received_date1}/quantity/{quantity}")
async def read_inventory_by_product_received_supplier_received_after_quantity(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date1, Inventory.quantity == quantity).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/after/{received_date1}/quantity/less/{quantity}")
async def read_inventory_by_product_received_supplier_received_after_quantity_less(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date1, Inventory.quantity < quantity).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/after/{received_date1}/quantity/more/{quantity}")
async def read_inventory_by_product_received_supplier_received_after_quantity_more(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date1, Inventory.quantity > quantity).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/after/{received_date1}/quantity/between/{quantity1}/{quantity2}")
async def read_inventory_by_product_received_supplier_received_after_quantity_between(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, quantity1: int, quantity2: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date > received_date1, Inventory.quantity.between(quantity1, quantity2)).all()
    return inventory

@router.get("/product/{product_id}/received/{received_date}/supplier/{supplier_id}/received/between/{received_date1}/{received_date2}/quantity/{quantity}")
async def read_inventory_by_product_received_supplier_received_between_quantity(product_id: int, received_date: datetime, supplier_id: int, received_date1: datetime, received_date2: datetime, quantity: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.received_date == received_date, Inventory.supplier_id == supplier_id, Inventory.received_date.between(received_date1, received_date2), Inventory.quantity == quantity).all()
    return inventory