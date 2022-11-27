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
from app.models.category import Categories
from . import categories_bp


@categories_bp.route("", methods=["POST"])
def create_category():
    pass

@categories_bp.route("", methods=["GET"])
def get_category():
    pass

@categories_bp.route("", methods=["PUT"])
def update_category():
    pass

@categories_bp.route("", methods=["DELETE"])
def delete_category():
    pass