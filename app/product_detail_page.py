from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)
from product_list import products_bp
from cart import cart_bp


@products_bp.route("", methods=["GET"])
def get_product_details():
    pass

@cart_bp.route("", methods=["POST"])
def add_to_cart():
    pass