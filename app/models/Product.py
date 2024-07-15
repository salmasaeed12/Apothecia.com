from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base



class Product(Base):
    __tablename__ = 'products'  # Corrected __tablename__

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

    category = relationship('Category', back_populates='products')
    order_details = relationship('OrderDetail', back_populates='product')
    inventory_entries = relationship('Inventory', back_populates='product')

