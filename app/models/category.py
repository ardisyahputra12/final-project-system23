from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
)


class Categories(Base, Histories):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)