<<<<<<< HEAD
mfrom . import Base
from app.utils.format_datetime import format_datetime
=======
from . import Base
from app.models.history import Histories
>>>>>>> f2aa20ea8497378289d897bf749f36aa0bd4d78c
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class Carts(Base, Histories):
    __tablename__ = 'carts'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    product_id = Column(String, ForeignKey('products.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)