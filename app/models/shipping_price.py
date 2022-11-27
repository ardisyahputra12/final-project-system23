from . import Base
from app.utils.format_datetime import format_datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class ShippingPrice(Base):
    __tablename__ = 'shipping_price'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cart_id = Column(String, ForeignKey('carts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String, nullable=False)           # shipping_method = "Same day" atau "Regular"/"Next day"
    price = Column(Integer, nullable=False)
    create_at = Column(String, nullable=True, server_default=f"{format_datetime()}")
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")