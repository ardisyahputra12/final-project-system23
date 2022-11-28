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
from app.models.order import Orders
from . import user_bp, sales_bp


@user_bp.route("", methods=["GET"])
@decode_auth_token
def user_details(current_user):
    pass

# Change to model Users
@user_bp.route("/shipping_address", methods=["POST"])
@decode_auth_token
def change_shipping_address(current_user):
    pass

# Get data from model Users
@user_bp.route("/shipping_address", methods=["GET"])
@decode_auth_token
def get_user_shipping_address(current_user):
    pass

@user_bp.route("/balance", methods=["POST"])
@decode_auth_token
def top_up_balance(current_user):
    pass

@user_bp.route("/balance", methods=["GET"])
@decode_auth_token
def get_user_balance(current_user):
    pass

@sales_bp.route("", methods=["GET"])
@decode_auth_token
def get_total_sales(current_user):
    pass