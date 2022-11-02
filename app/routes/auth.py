from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

sign_up_bp = Blueprint("sign_up", __name__, url_prefix="/sign-up")
sign_in_bp = Blueprint("sign_in", __name__, url_prefix="/sign-in")


@sign_up_bp.route("", methods=["POST"])
def sign_up():
    pass

@sign_in_bp.route("", methods=["POST"])
def sign_in():
    pass