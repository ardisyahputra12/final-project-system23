from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

order_bp = Blueprint("order", __name__, url_prefix="/order")
orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@order_bp.route("", methods=["GET"])
def user_orders():
    pass

@order_bp.route("", methods=["POST"])
def create_order():
    pass

@orders_bp.route("", methods=["GET"])
def get_orders():
    pass