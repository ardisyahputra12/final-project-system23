import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from app.utils.query import run_query
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import home_bp


@home_bp.route("/banner", methods=["GET"])
def get_image():
    query = run_query(select(Products.id, Products.image, Products.title).where(Products.condition!="soft_delete").limit(5))
    return success_message(200, data=query)


@home_bp.route("/category", methods=["GET"])
def get_category():
    query = run_query(select(Categories.id, Categories.title).where(Categories.status=="available"))
    for i in query:
        img = run_query(select(Products.image).where(Products.category_id==i["id"], Products.condition!="soft_delete").limit(1))
        i["image"] = img[0]["image"]
    return success_message(200, data=query)
