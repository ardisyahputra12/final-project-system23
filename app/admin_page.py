from utils import run_query, error_message, success_message
from blueprints import products_bp, categories_bp
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)
# from product_list import products_bp, categories_bp

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")
sales_bp = Blueprint("sales", __name__, url_prefix="/sales")


@orders_bp.route("", methods=["GET"])
def get_orders():
    pass

@products_bp.route("", methods=["POST"])
def create_product():
    pass

@products_bp.route("", methods=["PUT"])
def update_product():
    pass

@products_bp.route("", methods=["DELETE"])
def delete_product():
    pass

@categories_bp.route("", methods=["POST"])
def create_category():
    pass

@categories_bp.route("", methods=["PUT"])
def update_category():
    pass

@categories_bp.route("", methods=["DELETE"])
def delete_category():
    pass

@sales_bp.route("", methods=["GET"])
def get_total_sales():
    pass