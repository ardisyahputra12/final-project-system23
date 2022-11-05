from . import Base
from utils import format_datetime
from sqlalchemy import (
    Column,
    String,
)


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    create_at = Column(String, nullable=True, server_default=f"{format_datetime()}")
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")