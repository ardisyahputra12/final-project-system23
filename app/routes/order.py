import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from utils import (
    run_query,
    error_message,
    success_message,
    format_datetime,
)
from models.user import Users
from models.cart import Carts
from models.product import Products
from models.order import Orders
from . import order_bp, orders_bp


@order_bp.route("", methods=["POST"])
def create_order():
    pass

@order_bp.route("", methods=["GET"])
def user_orders():
    pass

@orders_bp.route("", methods=["GET"])
def get_orders():
    pass