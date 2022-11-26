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
from app.utils.auth_token import decode_auth_token
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
@decode_auth_token
def create_category(current_user):
    data = request.get_json()

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif ("category_name" not in data) or (data["category_name"] == ""):
        return error_message(400, "Unknown request, please check your request!")
    elif run_query(select(Categories.name).where(Categories.name==data["category_name"], Categories.status=="available")) == [{"name": data["category_name"]}]:
        return error_message(409, f"Category '{data['category_name']}' already exist")
    elif run_query(select(Categories.name).where(Categories.name==data["category_name"] and Categories.status=="soft_delete")) == [{"name": data["category_name"]}]:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(update(Categories).values(status="available", create_at=format_datetime(), create_by=user_name).where(Categories.name==data["category_name"] and Categories.status=="soft_delete"), True)
        return success_message(201, msg=f"Category '{data['category_name']}' added")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(insert(Categories).values(id=uuid.uuid4(), name=data["category_name"], create_at=format_datetime(), create_by=user_name), True)
        return success_message(201, msg=f"Category '{data['category_name']}' added")

@categories_bp.route("", methods=["GET"])
def get_category():
    if run_query(select(Categories).where(Categories.status == "available")) == []:
        return success_message(200, data="Category is empty")
    else:
        query = run_query(select(Categories.id, Categories.name).where(Categories.status=="available"))
        return success_message(200, data=query)

@categories_bp.route("/<category_id>", methods=["PUT"])
@decode_auth_token
def update_category(current_user, category_id):
    data = request.get_json()

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif (run_query(select(Categories.id).where(Categories.id==category_id and Categories.status=="available")) == []) or (run_query(select(Categories.status).where(Categories.id==category_id)) == [{"status": "soft_delete"}]):
        return error_message(400, "Category not found")
    elif (("category_name" not in data) or (data["category_name"] == "")) or (("category_id" not in data) or (data["category_id"] == "")):
        return error_message(400, "Unknown request, please check your request!")
    elif run_query(select(Categories.name).where(Categories.name==data["category_name"], Categories.status=="available")) == [{"name": data["category_name"]}]:
        return error_message(409, f"Category '{data['category_name']}' already exist")
    elif run_query(select(Categories.name).where(Categories.name==data["category_name"] and Categories.status=="soft_delete")) == [{"name": data["category_name"]}]:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        category_name = run_query(select(Categories.name).where(Categories.id==category_id))[0]["name"]
        run_query(update(Categories).values(id=data["category_id"], status="available", update_at=format_datetime(), update_by=user_name).where(Categories.name==data["category_name"] and Categories.status=="soft_delete"), True)
        run_query(update(Categories).values(status="soft_delete", update_at=format_datetime(), update_by=user_name).where(Categories.id==category_id and Categories.status=="available"), True)
        return success_message(200, msg=f"Category '{category_name}' updated to '{data['category_name']}'")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        category_name = run_query(select(Categories.name).where(Categories.id==category_id))[0]["name"]
        run_query(update(Categories).values(id=data["category_id"], name=data["category_name"], update_at=format_datetime(), update_by=user_name).where(Categories.id==category_id and Categories.status=="available"), True)
        return success_message(200, msg=f"Category '{category_name}' updated to '{data['category_name']}'")

@categories_bp.route("/<category_id>", methods=["DELETE"])
@decode_auth_token
def delete_category(current_user, category_id):
    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif (run_query(select(Categories.id).where(Categories.id==category_id and Categories.status=="available")) == []) or (run_query(select(Categories.status).where(Categories.id==category_id)) == [{"status": "soft_delete"}]):
        return error_message(400, "Category not found")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        category_name = run_query(select(Categories.name).where(Categories.id==category_id))[0]["name"]
        run_query(update(Categories).values(status="soft_delete", update_at=format_datetime(), update_by=user_name).where(Categories.id==category_id and Categories.status=="available"), True)
        return success_message(200, msg=f"Category '{category_name}' deleted")
