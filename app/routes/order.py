import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
    func
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
    
    for x in run_query(select(Carts.user_id, func.sum(Products.price*Carts.quantity)).filter(Carts.product_id==Products.id).where(Carts.user_id==current_user).group_by(Carts.user_id)):
        if method == "reguler":
            if x['sum_1'] < 200:
                total = int(x['sum_1']*(15/100))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    run_query(delete(Carts).where(Carts.user_id==current_user),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
            elif x['sum_1'] >= 200:
                total = int(x['sum_1']*(20/100))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    run_query(delete(Carts).where(Carts.user_id==current_user),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
        elif method == "next day":
            if x['sum_1'] < 300:
                total = int(x['sum_1']*(20/100))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    run_query(delete(Carts).where(Carts.user_id==current_user),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
            elif x['sum_1'] >= 300:
                total = int(x['sum_1']*(25/10))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    run_query(delete(Carts).where(Carts.user_id==current_user),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
            
    

@order_bp.route("", methods=["GET"])
@decode_auth_token
def user_orders(current_user):
    products_result=[]
    for x in run_query(select(Orders)):
        data = {"id":x['id'],"created_at":x['create_at'],"products":products_result,"shipping_method":x['shipping_method'],"shipping_address":x['shipping_address']}
        for x in run_query(select(Carts,Products).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
            products_result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["images_url"],"name":x["name"]})
    return success_message(200,data)
    
@orders_bp.route("", methods=["GET"])
@decode_auth_token
def get_orders(current_user):
    pass

@order_bp.route("/delete", methods=["GET"])
@decode_auth_token
def user_del(current_user):
    run_query(delete(Orders),True)
    return success_message(200,'delete')