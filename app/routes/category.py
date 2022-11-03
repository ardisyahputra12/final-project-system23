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
    # For testing only
    run_query(f"DELETE FROM categories", True)
    run_query(f"INSERT INTO categories VALUES ('cid1', 'baju', '{datetime.now()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid2', 'celana', '{datetime.now()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid3', 'kaos', '{datetime.now()}', 'admin')", True)
    # http://127.0.0.1:5000/categories

    query = run_query(f"SELECT category_id, category_name FROM categories")
    return success_message(200, query)

@categories_bp.route("", methods=["POST"])
def create_category():
    pass

@categories_bp.route("", methods=["PUT"])
def update_category():
    pass

@categories_bp.route("", methods=["DELETE"])
def delete_category():
    pass