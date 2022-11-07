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
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import products_bp


# first save image to model Images, then for column images url in model product fill the endpoint image
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