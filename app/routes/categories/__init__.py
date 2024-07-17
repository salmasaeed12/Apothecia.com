from fastapi import APIRouter, HTTPException
from app.models import Category, Product, Order, Inventory, OrderDetail, Supplier
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
#the atributte orders is a list of orders
@router.get("/{category_id}/products/{product_id}/orders")
async def product_orders(category_id: int, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    orders = product.orders
    db.close()
    return orders

@router.get("/{category_id}/products/{product_id}/orders/count")
async def product_orders_count(category_id: int, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    count = len(product.orders)
    db.close()
    return {"count": count}

@router.get("/{category_id}/products/{product_id}/orders/{order_id}")
async def product_order(category_id: int, product_id: int, order_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    order = db.query(Order).filter(Order.order_id == order_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{product_id}/orders")
async def create_order(product_id: int, user_id: int, quantity: int, total_price: float):
    db = SessionLocal()
    order = Order(user_id=user_id, total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)
    
    order_detail = Order.order_detail_id(order_id=order.id, product_id=product_id, quantity=quantity, price=total_price)
    db.add(order_detail)
    db.commit()
    
    db.close()
    return {"msg": "Order created successfully"}

@router.get("/{product_id}/orders")
async def product_order(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    orders = product.orders
    db.close()
    return orders

@router.get("/{product_id}/orders/count")
async def product_order_count(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    count = len(product.orders)
    db.close()
    return {"count": count}

@router.get("/{product_id}/orders/{order_id}")
async def product_order(product_id: int, order_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    order = db.query(Order).filter(Order.order_id == order_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{product_id}/orders/{order_id}")
async def update_order(product_id: int, order_id: int, user_id: int, quantity: int, total_price: float):
    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order.user_id = user_id
    order.total_price = total_price
    db.commit()
    db.close()
    return {"msg": "Order updated successfully"}

@router.delete("/{product_id}/orders/{order_id}")
async def delete_order(product_id: int, order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    db.close()
    return {"msg": "Order deleted successfully"}

@router.get("/{product_id}/orders/{order_id}/details")
async def order_details(product_id: int, order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    details = order.order_details
    db.close()
    return details

@router.get("/{product_id}/orders/{order_id}/details/count")
async def order_details_count(product_id: int, order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    count = len(order.order_details)
    db.close()
    return {"count": count}
#ordeldetails has a problem
@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}")
async def order_detail(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
    db.close()
    if detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return detail

@router.put("/{product_id}/orders/{order_id}/details/{order_detail_id}")
async def update_order_detail(product_id: int, order_id: int, order_detail_id: int, quantity: int, price: float, total_price: float):
    db = SessionLocal()
    detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
    if detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    detail.quantity = quantity
    detail.price = price
    detail.total_price = total_price
    db.commit()
    db.close()
    return {"msg": "Order detail updated successfully"}

@router.delete("/{product_id}/orders/{order_id}/details/{order_detail_id}")
async def delete_order_detail(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
    if detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    db.delete(detail)
    db.commit()
    db.close()
    return {"msg": "Order detail deleted successfully"}

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/product")
async def order_detail_product(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
    if detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    product = detail.product
    db.close()
    return product

@router.get("/{product_id}/orders/{order_id}/details/{order_detail_id}/order")
async def order_detail_order(product_id: int, order_id: int, order_detail_id: int):
    db = SessionLocal()
    detail = db.query(OrderDetail).filter(OrderDetail.order_detail_id == order_detail_id).first()
    if detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    order = detail.order
    db.close()
    return order

@router.get("/{category_id}/products/{product_id}/inventory")
async def product_inventory(category_id: int, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    inventory = product.inventory_entries
    db.close()
    return inventory

@router.get("/{category_id}/products/{product_id}/inventory/count")
async def product_inventory_count(category_id: int, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    count = len(product.inventory_entries)
    db.close()
    return {"count": count}

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}")
async def product_inventory_entry(category_id: int, product_id: int, inventory_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    db.close()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    return inventory

@router.put("/{category_id}/products/{product_id}/inventory/{inventory_id}")
async def update_inventory_entry(category_id: int, product_id: int, inventory_id: int, quantity: int, inventory_type: str):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    inventory.quantity = quantity
    inventory.type = inventory_type
    db.commit()
    db.close()
    return {"msg": "Inventory entry updated successfully"}

@router.delete("/{category_id}/products/{product_id}/inventory/{inventory_id}")
async def delete_inventory_entry(category_id: int, product_id: int, inventory_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    db.delete(inventory)
    db.commit()
    db.close()
    return {"msg": "Inventory entry deleted successfully"}

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/product")
async def inventory_entry_product(category_id: int, product_id: int, inventory_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    product = inventory.product
    db.close()
    return product

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier")
async def inventory_entry_supplier(category_id: int, product_id: int, inventory_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    supplier = inventory.supplier
    db.close()
    return supplier

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}")
async def inventory_entry_supplier(category_id: int, product_id: int, inventory_id: int, supplier_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    db.close()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory")
async def supplier_inventory(category_id: int, product_id: int, inventory_id: int, supplier_id: int):
    db = SessionLocal()
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    inventory = supplier.inventory_entries
    db.close()
    return inventory

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/count")
async def supplier_inventory_count(category_id: int, product_id: int, inventory_id: int, supplier_id: int):
    db = SessionLocal()
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    count = len(supplier.inventory_entries)
    db.close()
    return {"count": count}

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}")
async def supplier_inventory_entry(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int):
    db = SessionLocal()
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    inventory = db.query(Inventory).filter(Inventory.inventory_id == supplier_inventory_id).first()
    db.close()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    return inventory

@router.put("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}")
async def update_supplier_inventory_entry(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int, quantity: int, received_date: str):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == supplier_inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    inventory.quantity = quantity
    inventory.received_date = received_date
    db.commit()
    db.close()
    return {"msg": "Inventory entry updated successfully"}

@router.delete("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}")
async def delete_supplier_inventory_entry(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == supplier_inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    db.delete(inventory)
    db.commit()
    db.close()
    return {"msg": "Inventory entry deleted successfully"}

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}/product")
async def supplier_inventory_product(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == supplier_inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    product = inventory.product
    db.close()
    return product

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}/supplier")
async def supplier_inventory_supplier(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == supplier_inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    supplier = inventory.supplier
    db.close()
    return supplier

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}/supplier/{supplier_inventory_id}")
async def supplier_inventory_supplier(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int):
    db = SessionLocal()
    inventory = db.query(Inventory).filter(Inventory.inventory_id == supplier_inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    db.close()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}/supplier/{supplier_inventory_id}/inventory")
async def supplier_inventory(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int):
    db = SessionLocal()
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    inventory = supplier.inventory_entries
    db.close()
    return inventory

@router.get("/{category_id}/products/{product_id}/inventory/{inventory_id}/supplier/{supplier_id}/inventory/{supplier_inventory_id}/supplier/{supplier_inventory_id}/inventory/count")
async def supplier_inventory_count(category_id: int, product_id: int, inventory_id: int, supplier_id: int, supplier_inventory_id: int):
    db = SessionLocal()
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    count = len(supplier.inventory_entries)
    db.close()
    return {"count": count}