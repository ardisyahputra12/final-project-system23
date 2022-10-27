from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)
from profile_page import user_bp, order_bp

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")
shipping_price_bp = Blueprint("shipping_price", __name__, url_prefix="/shipping_price")


@cart_bp.route("", methods=["GET"])
def get_user_carts():
    pass

@user_bp.route("/shipping_address", methods=["GET"])
def get_user_shipping_address():
    pass

@shipping_price_bp.route("", methods=["GET"])
def get_shipping_price():
    pass

@order_bp.route("", methods=["POST"])
def create_order():
    pass

@cart_bp.route("", methods=["DELETE"])
def delete_cart_item():
    pass