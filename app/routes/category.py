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
from app.models.user import Users
from app.models.category import Categories
from . import categories_bp


# ==========================================================================
# # For testing only, to get user id
@categories_bp.route("/user", methods=["GET"])
def get_category_user():
    q = run_query(select(Users))
    return success_message(200, data=q)

@categories_bp.route("/all", methods=["GET"])
def get_category_all():
    q = run_query(select(Categories))
    return success_message(200, data=q)
# ==========================================================================

@categories_bp.route("", methods=["POST"])
def create_category():
    token = request.headers["Authentication"]
    data = request.get_json()

    if run_query(select(Users.id).where(Users.id==token)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==token)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif ("category_name" not in data) or (data["category_name"] == ""):
        return error_message(400, "Unknown request")
    elif run_query(select(Categories.name).where(Categories.name==data["category_name"])) == [{"name": data["category_name"]}]:
        return error_message(409, f"Category '{data['category_name']}' already exist")
    else:
        user_name = run_query(select(Users.name).where(Users.id==token))[0]["name"]
        run_query(insert(Categories).values(id=uuid.uuid4(), name=data["category_name"], create_at=format_datetime(), create_by=user_name), True)
        return success_message(201, msg=f"Category '{data['category_name']}' added")

@categories_bp.route("", methods=["GET"])
def get_category():
    token = request.headers["Authentication"]

    if run_query(select(Users.id).where(Users.id==token)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Categories)) == []:
        return success_message(200, data="Category is empty")
    else:
        query = run_query(select(Categories.id, Categories.name))
        return success_message(200, data=query)

@categories_bp.route("/<category_id>", methods=["PUT"])
def update_category(category_id):
    token = request.headers["Authentication"]
    data = request.get_json()

    if run_query(select(Categories.id).where(Categories.id==category_id)) == []:
        return error_message(400, "Category not found")
    elif run_query(select(Users.id).where(Users.id==token)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==token)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif (("category_name" not in data) or (data["category_name"] == "")) or (("category_id" not in data) or (data["category_id"] == "")):
        return error_message(400, "Unknown request")
    elif run_query(select(Categories.name).where(Categories.name==data["category_name"])) == [{"name": data["category_name"]}]:
        return error_message(409, f"Category '{data['category_name']}' already exist")
    elif run_query(select(Categories.id).where(Categories.id==data["category_id"])) == [{"id": data["category_id"]}]:
        return error_message(409, f"Id of category must be unique")
    else:
        user_name = run_query(select(Users.name).where(Users.id==token))[0]["name"]
        category_name = run_query(select(Categories.name).where(Categories.id==category_id))[0]["name"]
        run_query(update(Categories).values(id=data["category_id"], name=data["category_name"], update_at=format_datetime(), update_by=user_name).where(Categories.id==category_id), True)
        return success_message(200, msg=f"Category '{category_name}' updated to '{data['category_name']}'")

@categories_bp.route("/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    token = request.headers["Authentication"]

    if run_query(select(Categories.id).where(Categories.id==category_id)) == []:
        return error_message(400, "Category not found")
    elif run_query(select(Users.id).where(Users.id==token)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==token)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    else:
        category_name = run_query(select(Categories.name).where(Categories.id==category_id))[0]["name"]
        run_query(delete(Categories).where(Categories.id==category_id), True)
        return success_message(200, msg=f"Category '{category_name}' deleted")