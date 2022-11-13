from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class ShippingPrice(Base, Histories):
    __tablename__ = 'shipping_price'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cart_id = Column(String, ForeignKey('carts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String, nullable=False)           # shipping_method = "Same day" atau "Regular"/"Next day"
    price = Column(Integer, nullable=False)