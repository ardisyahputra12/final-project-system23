from . import Base
from utils import format_datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class Products(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True)
    category_id = Column(String, ForeignKey('categories.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    detail = Column(String, nullable=True, server_default="None")
    size = Column(String, nullable=True, server_default="['S', 'M', 'L']")
    condition = Column(String, nullable=False)          # condition == new/used/deleted
    image = Column(String, nullable=False)
    images_url = Column(String, nullable=True, server_default="[None]")
    create_at = Column(String, nullable=True, server_default=f"{format_datetime()}")
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")