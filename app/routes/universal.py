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
from . import universal_bp


@universal_bp.route("", methods=["GET"])
def get_image():
    # Only for tes
    return success_message(200, msg="Tes Success")