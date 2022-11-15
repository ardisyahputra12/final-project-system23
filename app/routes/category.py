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
from app.models.category import Categories
from . import categories_bp


@categories_bp.route("", methods=["POST"])
@decode_auth_token
def create_category(current_user):
    pass

@categories_bp.route("", methods=["GET"])
def get_category():
    pass

@categories_bp.route("", methods=["PUT"])
@decode_auth_token
def update_category(current_user):
    pass

@categories_bp.route("", methods=["DELETE"])
@decode_auth_token
def delete_category(current_user):
    pass