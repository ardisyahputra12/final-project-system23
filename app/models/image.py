from . import Base
from app.utils.format_datetime import format_datetime
from sqlalchemy import (
    Column,
    String,
)


class Images(Base):
    __tablename__ = 'images'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    create_at = Column(String, nullable=True, server_default=f"{format_datetime()}")
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")