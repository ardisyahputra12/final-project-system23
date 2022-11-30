import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
    and_,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import decode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import products_bp


# ==========================================================================
# For testing only, to get all products
@products_bp.route("/all", methods=["GET"])
def get_category_all():
    q = run_query(select(Products))
    return success_message(200, data=q)
# ==========================================================================


# First save image to model Images, then for column images url in model product fill the endpoint image
@products_bp.route("", methods=["POST"])
@decode_auth_token
def create_product(current_user):
    body = request.get_json()

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif ("category" not in body) or (body["category"] == ""):
        return error_message(400, "Category can't empty, please check your request!")
    elif type(body["category"]) != str:
        return error_message(400, "Type of category must be string")
    elif run_query(select(Categories.id).where(Categories.id==body["category"], Categories.status=="available")) == []:
        return error_message(400, "Category not found")
    elif ("product_name" not in body) or (body["product_name"] == ""):
        return error_message(400, "Product_name can't empty, please check your request!")
    elif type(body["product_name"]) != str:
        return error_message(400, "Type of product_name must be string")
    elif ("price" not in body) or (body["price"] == "") or (body["price"] == None):
        return error_message(400, "Price can't empty, please check your request!")
    elif type(body["price"]) != int:
        return error_message(400, "Type of price must be number or integer")
    elif body["price"] < 1:
        return error_message(400, "Price must be positive numbers")
    elif ("condition" not in body) or (body["condition"] == ""):
        return error_message(400, "Condition can't empty, please check your request!")
    elif type(body["condition"]) != str:
        return error_message(400, "Type of condition must be string")
    elif (body["condition"] != "new") and (body["condition"] != "used"):
        return error_message(400, "Fill condition with only 'new' or 'used'")
    elif ("images" not in body) or (body["images"] == ""):
        return error_message(400, "Images can't empty, please check your request!")
    elif type(body["images"]) != str:
        return error_message(400, "Type of images must be string")
    elif ("description" not in body) or (body["description"] == ""):
        return error_message(400, "Description can't empty, please check your request!")
    elif type(body["description"]) != str:
        return error_message(400, "Type of description must be string")
    elif body["description"].count("")-1 < 50:
        return error_message(400, f"Description less than 50 characters, add {50 - (body['description'].count('')-1)} characters more")
    elif run_query(select(Products.name, Products.category_id, Products.condition).distinct().where(and_(Products.name==body["product_name"], Products.category_id==body["category"], Products.condition==body["condition"]))) == [{"name": body["product_name"], "category_id": body["category"], "condition": body["condition"]}]:
        return error_message(409, f"Product '{body['product_name']}' already exist")
    elif run_query(select(Products.name, Products.category_id).distinct().where(and_(Products.name==body["product_name"], Products.category_id==body["category"], Products.condition=="soft_delete"))) == [{"name": body["product_name"], "category_id": body["category"]}]:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(update(Products).values(price=body["price"], condition=body["condition"], images_url=str(body["images"]), detail=body["description"], create_at=format_datetime(), create_by=user_name).where(and_(Products.name==body["product_name"], Products.category_id==body["category"], Products.condition=='soft_delete')), True)
        return success_message(201, f"Product '{body['product_name']}' added")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(insert(Products).values(id=uuid.uuid4(), category_id=body["category"], name=body["product_name"], price=body["price"], condition=body["condition"], images_url=body["images"], detail=body["description"], create_at=format_datetime(), create_by=user_name), True)
        return success_message(201, f"Product '{body['product_name']}' added")

@products_bp.route("", methods=["GET"])
def get_product_list():
    params = request.args
    page = params.get("page", default=1, type=int)
    page_size = params.get("page_size", default=20, type=int)
    sort_by = params.get("sort_by", default="price_a_z", type=str)
    category = params.get("category", type=str)
    price = params.get("price", default=999999999999, type=int)
    condition = params.get("condition", type=str)
    product_name = params.get("product_name", type=str)

    if run_query(select(Products).where(Products.condition != "soft_delete")) == []:
        return success_message(200, data="Product is empty")
    elif (page != None and page < 1) or (page_size != None and page_size < 1) or (price != None and price < 1):
        return error_message(400, "Params Page, page size, and price must be positive numbers")
    else:
        sort = 'ASC'
        where = ""
        if sort_by == "price_z_a": sort = 'DESC'
        elif (sort_by != "") and (sort_by != "price_z_a") and (sort_by != "price_a_z"):
            return error_message(400, "Params sort_by unknown, please use price_z_a or price_a_z")
        if category != "" and category != None:
            where += f"category_id='{category}' and "
        if product_name != "" and product_name != None:
            where += f"name LIKE '%{product_name}%' and "
        if condition != "" and condition != None:
            where += f"condition='{condition}' and "
        query = run_query(
            f"""SELECT id, images_url, name, price
                FROM products
                WHERE {where} price<={price} and condition!='soft_delete'
                ORDER BY price {sort}
                LIMIT {page_size}
            """
        )
        return success_message(200, data=query, row=True)

@products_bp.route("", methods=["PUT"])
@decode_auth_token
def update_product(current_user):
    body = request.get_json()

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif ("product_name" not in body) or (body["product_name"] == ""):
        return error_message(400, "Product_name can't empty, please check your request!")
    elif type(body["product_name"]) != str:
        return error_message(400, "Type of product_name must be string")
    elif ("product_id" not in body) or (body["product_id"] == ""):
        return error_message(400, "Product_id can't empty, please check your request!")
    elif type(body["product_id"]) != str:
        return error_message(400, "Type of product_id must be string")
    elif (run_query(select(Products.id).where(Products.id==body["product_id"], Products.condition!='soft_delete')) == []) or (run_query(select(Products.condition).where(Products.id==body["product_id"])) == [{"condition": "soft_delete"}]):
        return error_message(400, "Product not found")
    elif ("category" not in body) or (body["category"] == ""):
        return error_message(400, "Category can't empty, please check your request!")
    elif type(body["category"]) != str:
        return error_message(400, "Type of category must be string")
    elif run_query(select(Categories.id).where(Categories.id==body["category"], Categories.status=="available")) == []:
        return error_message(400, "Category not found")
    elif ("price" not in body) or (body["price"] == "") or (body["price"] == None):
        return error_message(400, "Price can't empty, please check your request!")
    elif type(body["price"]) != int:
        return error_message(400, "Type of price must be number or integer")
    elif body["price"] < 1:
        return error_message(400, "Price must be positive numbers, please check your request!")
    elif ("condition" not in body) or (body["condition"] == ""):
        return error_message(400, "Condition can't empty, please check your request!")
    elif type(body["condition"]) != str:
        return error_message(400, "Type of condition must be string")
    elif (body["condition"] != "new") and (body["condition"] != "used"):
        return error_message(400, "Fill condition with only 'new' or 'used', please check your request!")
    elif ("description" not in body) or (body["description"] == ""):
        return error_message(400, "Description can't empty, please check your request!")
    elif type(body["description"]) != str:
        return error_message(400, "Type of description must be string")
    elif body["description"].count("")-1 < 50:
        return error_message(400, f"Description less than 50 characters, add {50 - (body['description'].count('')-1)} characters more, please check your request!")
    elif ("images" not in body) or (body["images"] == ""):
        return error_message(400, "Images can't empty, please check your request!")
    elif type(body["images"]) != str:
        return error_message(400, "Type of images must be string")
    elif run_query(select(Products.name, Products.category_id, Products.condition, Products.price, Products.images_url, Products.detail).distinct().where(and_(Products.name==body["product_name"], Products.category_id==body["category"], Products.condition==body["condition"]))) == [{"name": body["product_name"], "category_id": body["category"], "condition": body["condition"], "price": body["price"], "images_url":body["images"], "detail":body["description"]}]:
        return error_message(409, f"Product '{body['product_name']}' already exist")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(update(Products).values(id=body["product_id"], category_id=body["category"], name=body["product_name"], price=body["price"], condition=body["condition"], images_url=str(body["images"]), detail=body["description"], update_at=format_datetime(), update_by=user_name).where(and_(Products.id==body["product_id"], Products.condition!="soft_delete")), True)
        return success_message(200, f"Product '{body['product_id']}' updated")

@products_bp.route("", methods=["DELETE"])
@decode_auth_token
def delete_product(current_user):
    product_id = request.args.get("product_id", type=str)

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif (run_query(select(Products.id).where(Products.id==product_id and Products.condition!='soft_delete')) == []) or (run_query(select(Products.condition).where(Products.id==product_id)) == [{"condition": "soft_delete"}]):
        return error_message(400, "Product not found")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        product_name = run_query(select(Products.name).where(Products.id==product_id))[0]["name"]
        run_query(update(Products).values(condition="soft_delete", update_at=format_datetime(), update_by=user_name).where(Products.id==product_id and Products.condition!="soft_delete"), True)
        return success_message(200, f"Product '{product_name}' deleted")

@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    # http://127.0.0.1:5000/products/search_image
    body = request.get_json()
    if ("image" not in body) or (body["image"] == ""): return error_message(400, "Can't search image, image is empty!")
    query = run_query(f"SELECT DISTINCT category_id FROM products WHERE images_url LIKE '%{body['image']}%'")
    return success_message(200, key="result", data=query)

@products_bp.route("/<id>", methods=["GET"])
def get_product_details(id):
    if (run_query(select(Products.id).where(Products.id==id, Products.condition!='soft_delete')) == []) or (run_query(select(Products.condition).where(Products.id==id)) == [{"condition": "soft_delete"}]):
        return error_message(404, "Product not found")
    elif [{"id": id}] == run_query(select(Products.id).where(Products.id==id)):
        query = run_query(select(Products.id, Products.name, Products.size, Products.detail, Products.price, Products.images_url).where(Products.id==id))
        return success_message(200, msg=query)
    else: return error_message(404, "Not Found")
