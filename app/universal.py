from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

universal_bp = Blueprint("universal", __name__, url_prefix="/image")


@universal_bp.route("", methods=["GET"])
def get_image():
    # Only for tes
    return success_message("Tes Success", 200)