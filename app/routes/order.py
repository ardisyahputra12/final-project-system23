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
from app.models.cart import Carts
from app.models.product import Products
from app.models.order import Orders
from . import order_bp, orders_bp


@order_bp.route("", methods=["POST"])
@decode_auth_token
def create_order(current_user):
    body = request.json
    method = body.get("shipping_method")
    address = body.get("shipping_address")
    user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]

    shipping_method = [{"name": "regular", "price": 0}, {"name": "next day", "price": 0}]
    products_in_cart = run_query(select(Carts.quantity, Products.price).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user))
    total_price = sum(float(val["price"] * val["quantity"]) for val in products_in_cart)

    regular_price = (15*total_price)/100 if total_price < 200 else (20*total_price)/100
    shipping_method[0]["price"] = int(regular_price)

    next_day_price = (20*total_price)/100 if total_price < 300 else (25*total_price)/100
    shipping_method[1]["price"] = int(next_day_price)

    def order(val):
        if shipping_method[val]["price"] > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
            return error_message(401,"your balance is not enough")
        else:
            products_result=[]
            for x in run_query(select(Orders).where(Orders.user_id==current_user)):
                for x in run_query(select(Carts,Products.image,Products.price,Products.title).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
                    products_result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["image"],"name":x["title"]})
                run_query(delete(Carts).where(Carts.user_id==current_user),True)
            run_query(insert(Orders).values(products=products_result,id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(shipping_method[val]["price"]),create_at=format_datetime(),create_by=user_name),True)
            run_query(update(Users).values(balance=Users.balance-shipping_method[val]["price"]).where(Users.id==current_user),True)
            run_query(update(Users).values(balance=Users.balance+shipping_method[val]["price"]).where(Users.is_admin==True), True)
            return success_message(200,"order success")

    for x in run_query(select(Carts.user_id).where(Carts.user_id==current_user)):
        if method == "regular": return order(0)
        elif method == "next day": return order(1)


@orders_bp.route("", methods=["GET"])
@decode_auth_token
def get_orders(current_user):
    data=[]
    for x in run_query(select(Users).where(Users.is_admin==False)):
        for z in run_query(select(Orders).where(Orders.user_id==x['id']).group_by(Orders.id)):
            order_id = z['id']
            create_at = z['create_at']
            for a in z['products']:
                total = a['price']
            data.append({"id":order_id,"user_name":x['name'],"created_at":create_at,"user_id":x['id'],"user_email":x['email'],"total": total})
    return success_message(200,data)
