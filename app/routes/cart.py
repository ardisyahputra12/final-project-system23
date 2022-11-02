from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")
shipping_price_bp = Blueprint("shipping_price", __name__, url_prefix="/shipping_price")


@cart_bp.route("", methods=["GET"])
def get_user_carts():
    pass

@cart_bp.route("", methods=["POST"])
def add_to_cart():
    pass

@cart_bp.route("", methods=["DELETE"])
def delete_cart_item():
    pass

@shipping_price_bp.route("", methods=["GET"])
def get_shipping_price():
    pass