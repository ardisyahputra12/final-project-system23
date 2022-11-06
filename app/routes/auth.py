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
from models.user import Users
from . import sign_up_bp, sign_in_bp


@sign_up_bp.route("", methods=["POST"])
def sign_up():
    pass

@sign_in_bp.route("", methods=["POST"])
def sign_in():
    pass