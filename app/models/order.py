from . import Base
from utils import format_datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    JSON,
    ForeignKey,
)


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    product_id = Column(String, ForeignKey('products.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cart_id = Column(String, ForeignKey('carts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    shipping_method = Column(String, nullable=False)
    shipping_address = Column(JSON, nullable=False)
    status = Column(String, nullable=True, server_default="waiting")        # status = waiting/succeed/canceled
    total_price = Column(Integer, nullable=False)
    create_at = Column(String, nullable=True, server_default=f"{format_datetime()}")
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")