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
from models.product import Products
from models.cart import Carts
from models.shipping_price import ShippingPrice
from . import cart_bp, shipping_price_bp


@cart_bp.route("", methods=["POST"])
def add_to_cart():
    pass

@cart_bp.route("", methods=["GET"])
def get_user_carts():
    pass

@cart_bp.route("", methods=["DELETE"])
def delete_cart_item():
    pass

@shipping_price_bp.route("", methods=["GET"])
def get_shipping_price():
    pass