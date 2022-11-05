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
from . import home_bp


@home_bp.route("/banner", methods=["GET"])
def get_image():
    pass

@home_bp.route("/category", methods=["GET"])
def get_category():
    pass