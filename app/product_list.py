from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

products_bp = Blueprint("products", __name__, url_prefix="/products")
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@products_bp.route("", methods=["GET"])
def get_product_list():
    pass

@categories_bp.route("", methods=["GET"])
def get_category():
    pass

@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    pass