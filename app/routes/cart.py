import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
    alias,
    func
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import decode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.category import Categories
from app.models.user import Users
from app.models.product import Products
from app.models.cart import Carts
from app.models.shipping_price import ShippingPrice
from . import cart_bp, shipping_price_bp


@cart_bp.route("", methods=["POST"])
@decode_auth_token
def add_to_cart(current_user):
    # IMPLEMENT THIS
    body = request.json
    product_id = body.get("id")
    quantity = body.get("quantity")
    size = body.get("size")
    
    
    run_query(f"DELETE FROM categories", True)
    run_query(insert(Categories).values(id='cid1',title='baju',status='available',create_at=format_datetime(),create_by='admin'),True)
    run_query(insert(Categories).values(id='cid2',title='celana',status='available',create_at=format_datetime(),create_by='admin'),True)
    run_query(insert(Products).values(name='baju',price='200',condition='new',detail='detail',id='pid1',images_url='images_1',size='M',create_at=format_datetime(),create_by='admin',category_id='cid1'),True)
    run_query(insert(Products).values(name='baju',price='250',condition='soft',detail='detail',id='pid2',images_url='images_2',size='XL',create_at=format_datetime(),create_by='admin',category_id='cid1'),True)
    run_query(insert(Products).values(name='celana',price='150',condition='new',detail='detail',id='pid3',images_url='images_3',size='S',create_at=format_datetime(),create_by='admin',category_id='cid2'),True)
    
    
    user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
    if product_id == None or quantity == None or size == None:
        return error_message(400,"invalid product")
    else:
        run_query(insert(Carts).values(id=uuid.uuid4(),user_id=current_user,product_id=product_id,size=size,quantity=quantity,create_at=format_datetime(),create_by=user_name),True)
        return success_message(200,"item add to cart")
    

@cart_bp.route("", methods=["GET"])
@decode_auth_token
def get_user_carts(current_user):
    result = []
    for x in run_query(select(Carts,Products).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
        result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["images_url"],"name":x["name"]})
    return result

@cart_bp.route("", methods=["DELETE"])
@decode_auth_token
def delete_cart_item(current_user):
    # IMPLEMENT THIS
    req = request.args
    cart_id = req.get("cart_id")
    if run_query(select(Carts.user_id).where(Carts.user_id==current_user))!=None:
        run_query(delete(Carts).where(Carts.id==cart_id),True)
        return success_message(201,"Cart deleted")
    if run_query(select(Carts.id).where(Carts.id==cart_id))==None:
        return error_message(400,"item not found")
    
# Get shipping price after push data to model ShippingPrice in endpoint add to cart
@shipping_price_bp.route("", methods=["GET"])
@decode_auth_token
def get_shipping_price(current_user):
    for x in run_query(select(Carts.user_id, func.sum(Products.price*Carts.quantity)).filter(Carts.product_id==Products.id).where(Carts.user_id==current_user).group_by(Carts.user_id)):
        if x['sum_1'] < 200:
            reguler = format(x['sum_1'])*(15/100)
        elif x['sum_1'] >= 200:
            reguler = format(x['sum_1']*(20/100))
        if x['sum_1'] < 300:
            next_day = format(x['sum_1'])*(20/100)
        elif x['sum_1'] >= 300:
            next_day = format(x['sum_1']*(25/100))
            
        result = [{"name":"reguler","price":reguler},{"name":"next day","price":next_day}]
    
    return result