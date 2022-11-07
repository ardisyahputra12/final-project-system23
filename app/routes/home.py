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
from . import home_bp


@home_bp.route("/banner", methods=["GET"])
def get_image():
    pass

@home_bp.route("/category", methods=["GET"])
def get_category():
    pass