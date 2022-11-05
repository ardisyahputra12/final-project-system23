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
from models.product import Products
from models.category import Categories
from . import products_bp


@products_bp.route("", methods=["POST"])
def create_product():
    pass

@products_bp.route("", methods=["GET"])
def get_product_list():
    pass

@products_bp.route("", methods=["PUT"])
def update_product():
    pass

@products_bp.route("", methods=["DELETE"])
def delete_product():
    pass

@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    pass

@products_bp.route("/<id>", methods=["GET"])
def get_product_details(id):
    pass