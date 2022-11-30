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
<<<<<<< HEAD
def add_to_cart():
    # IMPLEMENT THIS
    header = request.headers
    body = request.json
    id_product = body.get("id")
    quantity = body.get("quantity")
    size = body.get("size")
    token = header.get("Authentication")

    #TABLE INIT(tidak dipakai lagi)
    '''
    users = Table('users', MetaData(bind=get_engine()), autoload=True)
    products = Table('products', MetaData(bind=get_engine), autoload=True)
    carts = Table('carts', MetaData(bind=get_engine), autoload=True)
    '''

    #IDENFITY USER AND TOKEN
    user = run_query(select(users.id).where(users.id == token))
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
=======
@decode_auth_token
def add_to_cart(current_user):
    pass
>>>>>>> f2aa20ea8497378289d897bf749f36aa0bd4d78c

@cart_bp.route("", methods=["GET"])
@decode_auth_token
def get_user_carts(current_user):
    pass

@cart_bp.route("", methods=["DELETE"])
<<<<<<< HEAD
def delete_cart_item():
    # IMPLEMENT THIS
    header = request.headers
    token = header.get("Authentication")

    #TABLE INIT(tidak dipakai lagi)
    '''
    users = Table("users", MetaData(bind=get_engine()), autoload=True)
    carts = Table("carts", MetaData(bind=get_engine()), autoload=True)
    '''

    user = run_query(select(users).where(users.c.token == token))

    if len(user) == 0:
        return {"message": "error, user is invalid"}, 400
    else:
        run_query(delete(carts).where(carts.id_cart == cart_id))
        return {"message": "Cart deleted"}, 200

=======
@decode_auth_token
def delete_cart_item(current_user):
>>>>>>> f2aa20ea8497378289d897bf749f36aa0bd4d78c
    pass

# Get shipping price after push data to model ShippingPrice in endpoint add to cart
@shipping_price_bp.route("", methods=["GET"])
@decode_auth_token
def get_shipping_price(current_user):
    pass