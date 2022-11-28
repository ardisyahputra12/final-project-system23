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
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import products_bp


# first save image to model Images, then for column images url in model product fill the endpoint image
@products_bp.route("", methods=["POST"])
@decode_auth_token
def create_product(current_user):
    pass

@products_bp.route("", methods=["GET"])
def get_product_list():
    pass

@products_bp.route("", methods=["PUT"])
@decode_auth_token
def update_product(current_user):
    pass

@products_bp.route("", methods=["DELETE"])
@decode_auth_token
def delete_product(current_user):
    pass

@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    pass

@products_bp.route("/<id>", methods=["GET"])
def get_product_details(id):
    pass