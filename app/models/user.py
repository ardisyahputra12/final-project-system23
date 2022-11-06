from . import Base
from utils import format_datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
)


class Users(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    type = Column(String, nullable=False)               # type = seller/buyer
    is_admin = Column(Boolean, nullable=True, server_default="False")
    balance = Column(Integer, nullable=True, server_default="0")
    create_at = Column(String, nullable=True, server_default=f"{format_datetime()}")
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")