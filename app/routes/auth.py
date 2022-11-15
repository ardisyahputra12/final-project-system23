import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import encode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from . import sign_up_bp, sign_in_bp


@sign_up_bp.route("", methods=["POST"])
def sign_up():
    pass

@sign_in_bp.route("", methods=["POST"])
def sign_in():
    # For example only
    name = request.get_json()["name"]
    user_id = run_query(select(Users.id).where(Users.name==name))[0]["id"]
    token = encode_auth_token(user_id)
    return success_message(200, data="Login success", key="message", tkn=token)