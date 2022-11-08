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
    # For testing only
    run_query(f"DELETE FROM categories", True)
    run_query(f"INSERT INTO categories VALUES ('cid1', 'baju', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid2', 'celana', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid3', 'kaos', '{format_datetime()}', 'admin')", True)
    # http://127.0.0.1:5000/categories

    query = run_query(f"SELECT id, name FROM categories")
    return success_message(200, query)

@categories_bp.route("", methods=["PUT"])
def update_category():
    pass

@categories_bp.route("", methods=["DELETE"])
def delete_category():
    pass