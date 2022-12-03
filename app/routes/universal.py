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
from app.models.image import Images
from . import universal_bp


@universal_bp.route("/<name>", methods=["GET"])
def get_image(name):
    pass