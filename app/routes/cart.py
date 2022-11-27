import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from app.utils.query import run_query
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
    # IMPLEMENT THIS
    header = request.headers
    body = request.json
    id_product = body.get("id")
    quantity = body.get("quantity")
    size = body.get("size")
    token = header.get("Authentication")

    #TABLE INIT
    users = Table('users', MetaData(bind=get_engine()), autoload=True)
    products = Table('products', MetaData(bind=get_engine), autoload=True)
    carts = Table('carts', MetaData(bind=get_engine), autoload=True)

    #IDENFITY USER AND TOKEN
    user = run_query(select(users.c.id_user).where(users.c.token == token))

    if user == False:
        return {"messege": "error, user is invalid"}, 400
    else:
        data = {
            "id_cart": str(uuid.uuid4()),
            "user_id": user,
            "product_id": product_id,
            "quantity": quantity,
            "size": size
        }

    run_query(insert(carts).values(data),commit=True)
    return {"message" : "item added to cart"}, 201

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