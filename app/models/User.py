from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from ..database import Base
from enum import Enum as PyEnum


class UserRole(PyEnum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = 'users'  # Corrected __tablename__

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(50))
    address = Column(Text)
    role = Column(Enum(UserRole), default=UserRole.user)

    orders = relationship('Order', back_populates='user')
