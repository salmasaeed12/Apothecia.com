from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base



class Order(Base):
    __tablename__ = 'orders'  # Corrected __tablename__

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    order_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)

    user = relationship('User', back_populates='orders')
    order_details = relationship('OrderDetail', back_populates='order')


class OrderDetail(Base):
    __tablename__ = 'order_details'  # Corrected __tablename__

    order_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details')

