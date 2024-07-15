from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class Inventory(Base):
    __tablename__ = 'inventory'  # Corrected __tablename__

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    quantity = Column(Integer, nullable=False)
    received_date = Column(DateTime, nullable=False)

    product = relationship('Product', back_populates='inventory_entries')
    supplier = relationship('Supplier', back_populates='inventory_entries')
