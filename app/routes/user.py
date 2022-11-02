from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

user_bp = Blueprint("user", __name__, url_prefix="/user")
sales_bp = Blueprint("sales", __name__, url_prefix="/sales")


@user_bp.route("", methods=["GET"])
def user_details():
    pass

@user_bp.route("/shipping_address", methods=["GET"])
def get_user_shipping_address():
    pass

@user_bp.route("/shipping_address", methods=["POST"])
def change_shipping_address():
    pass

@user_bp.route("/balance", methods=["GET"])
def get_user_balance():
    pass

@user_bp.route("/balance", methods=["POST"])
def top_up_balance():
    pass

@sales_bp.route("", methods=["GET"])
def get_total_sales():
    pass