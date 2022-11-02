from utils import run_query, error_message, success_message
from datetime import datetime
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("", methods=["GET"])
def get_category():
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