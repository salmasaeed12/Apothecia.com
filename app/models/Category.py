from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base


class Category(Base):
    __tablename__ = 'categories'  # Corrected __tablename__

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)

    products = relationship('Product', back_populates='category')
