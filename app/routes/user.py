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
from app.models.order import Orders
from . import user_bp, sales_bp


@user_bp.route("", methods=["GET"])
def user_details():
    pass

# Change to model Users
@user_bp.route("/shipping_address", methods=["POST"])
def change_shipping_address():
    pass

# Get data from model Users
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