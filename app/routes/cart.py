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
from app.utils.auth_token import decode_auth_token
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
@decode_auth_token
def add_to_cart(current_user):
    pass

@cart_bp.route("", methods=["GET"])
@decode_auth_token
def get_user_carts(current_user):
    pass

@cart_bp.route("", methods=["DELETE"])
@decode_auth_token
def delete_cart_item(current_user):
    pass

# Get shipping price after push data to model ShippingPrice in endpoint add to cart
@shipping_price_bp.route("", methods=["GET"])
@decode_auth_token
def get_shipping_price(current_user):
    pass