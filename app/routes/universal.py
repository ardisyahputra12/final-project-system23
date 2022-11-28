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


@universal_bp.route("/image", methods=["GET"])
def get_image():
    send_file(io.BytesIO(content), mimetype=f"image/{extension}")

@universal_bp.route("/<name>", methods=["GET"])
def get_image(name):
<<<<<<< HEAD
    f141ba56ad053241ebb0627e351f6ac20184d382
    # Only for tes
    return success_message(200, msg="Tes Success")
=======
    pass
>>>>>>> f2aa20ea8497378289d897bf749f36aa0bd4d78c
