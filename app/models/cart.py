from . import Base
from utils import format_datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class Carts(Base):
    __tablename__ = 'carts'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    product_id = Column(String, ForeignKey('products.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    create_at = Column(String, nullable=True, server_default=f"{format_datetime()}")
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")