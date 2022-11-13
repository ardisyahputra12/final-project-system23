import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from app.models.product import Products
from app.models.cart import Carts
from app.models.shipping_price import ShippingPrice
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

# Get shipping price after push data to model ShippingPrice in endpoint add to cart
@shipping_price_bp.route("", methods=["GET"])
def get_shipping_price():
    pass