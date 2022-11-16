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
from models.order import Orders
from . import user_bp, sales_bp


@user_bp.route("", methods=["GET"])
def user_details():
    req = request.args
    id = req.get("id")
    
    # if id == None:
    #     return run_query (f"select name,email,phone_number from users")
    # else:
    #     return run_query(f"select name,email,phone_number from users where id = '{id}'")
    
    return run_query (f"select name,email,phone_number from users")

# Change to table Users and column shipping_address in table Orders
@user_bp.route("/shipping_address", methods=["POST"])
def change_shipping_address():
    pass

# Get data from table user
@user_bp.route("/shipping_address", methods=["GET"])
def get_user_shipping_address():
    pass

@user_bp.route("/balance", methods=["POST"])
def top_up_balance():
    pass

@user_bp.route("/balance", methods=["GET"])
def get_user_balance():
    pass

@sales_bp.route("", methods=["GET"])
def get_total_sales():
    pass