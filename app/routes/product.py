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
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import products_bp


# first save image to model Images, then for column images url in model product fill the endpoint image
@products_bp.route("", methods=["POST"])
@decode_auth_token
def create_product(current_user):
    body = request.get_json()
    category = body["category"]
    product_name = body["product_name"]
    price = body["price"]
    condition = body["condition"]
    images = body["images"]
    description = body["description"]

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user.")
    elif category == "":
        return error_message(400, "Category can't empty.")
    elif run_query(select(Categories.id).where(Categories.id==category and Categories.status=="available")) == []:
        return error_message(400, "Category not found.")
    elif product_name == "":
        return error_message(400, "Product_name can't empty.")
    elif price == "" or price == None:
        return error_message(400, "Price can't empty.")
    elif price < 1:
        return error_message(400, "Price must be positive numbers.")
    elif condition == "":
        return error_message(400, "Condition can't empty.")
    elif condition != "new" or condition != "used":
        return error_message(400, "Fill condition with only 'new' or 'used'")
    elif images == "":
        return error_message(400, "Images can't empty.")
    elif description == "":
        return error_message(400, "Description can't empty.")
    elif description.count("")-1 < 50:
        return error_message(400, f"Description less than 50 characters, add {50 - (description.count('')-1)} characters more.")
    elif run_query(select(Products.name, Products.category_id, Products.condition).where(Products.name==product_name and Products.category_id==category and Products.condition==condition and Products.condition!='soft_delete')) == [{"name": product_name, "category_id": category, "condition": condition}]:
        return error_message(409, f"Product '{product_name}' already exist.")
    elif run_query(select(Products.name, Products.category_id).where(Products.name==product_name and Products.category_id==category and Products.condition=='soft_delete')) == [{"name": product_name, "category_id": category}]:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(update(Products).values(price=price, condition=condition, images_url=str(images), detail=description, create_at=format_datetime(), create_by=user_name).where(Products.name==product_name and Products.category_id==category and Products.condition=='soft_delete'), True)
        return success_message(200, f"Product '{product_name}' added.")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(insert(Products).values(id=uuid.uuid4(), category_id=category, name=product_name, price=price, condition=condition, images_url=images, detail=description, create_at=format_datetime(), create_by=user_name), True)
        return success_message(201, f"Product '{product_name}' added.")

@products_bp.route("", methods=["GET"])
def get_product_list():
    params = request.args
    page = params.get("page", type=int)
    page_size = params.get("page_size", type=int)
    sort_by = params.get("sort_by", type=str)
    category = params.get("category", type=str)
    price = params.get("price", type=int)
    condition = params.get("condition", type=str)
    product_name = params.get("product_name", type=str)

    # For testing only
    # run_query(delete(Products), True)
    # run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid1", name="baju", price=60, condition="used", images_url="image1", detail="lorem", create_by='Saya'), True)
    # run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid1", name="baju", price=100, condition="used", images_url="image1", detail="lorem", create_by='Saya'), True)
    # run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid1", name="baju", price=99, condition="used", images_url="image2", detail="lorem", create_by='Saya'), True)
    # run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid2", name="celana", price=110, condition="used", images_url="image2", detail="lorem", create_by='Saya'), True)
    # http://127.0.0.1:5000/products?category=cid1&price=100&product_name=baju&condition=used&sort_by=price_a_z

    if category == None or price == None or product_name == None or condition == None:
        return error_message(400, "Params category, price, product_name, and condition can't empty")
    elif (page != None and page < 1) or (page_size != None and page_size < 1) or (price != None and price < 1):
        return error_message(400, "Params Page, page size, and price must be positive numbers")
    else:
        if page_size==None: page_size=20
        if sort_by == "price_z_a": sort = 'DESC'
        elif sort_by == "price_a_z" or sort_by == None: sort = 'ASC'
        else: return error_message(400, "Params sort_by unknown, please use price_z_a or price_a_z")
        query = run_query(
            f"""SELECT id, images_url, name, price
                FROM products
                WHERE category_id='{category}' and price<={price} and name='{product_name}' and condition='{condition}' and condition!='soft_delete'
                ORDER BY price {sort}
                LIMIT {page_size}
            """
        )
        return success_message(200, data=query, row=True)

@products_bp.route("", methods=["PUT"])
@decode_auth_token
def update_product(current_user):
    body = request.get_json()
    product_id = body["product_id"]
    category = body["category"]
    product_name = body["product_name"]
    price = body["price"]
    condition = body["condition"]
    images = body["images"]
    description = body["description"]

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user.")
    elif (run_query(select(Products.id).where(Products.id==product_id and Products.condition!='soft_delete')) == []) or (run_query(select(Products.id).where(Products.id==product_id and Products.condition=='soft_delete')) != []):
        return error_message(400, "Product not found.")
    elif (run_query(select(Categories.id).where(Categories.id==category and Categories.status=="available")) == []) or (run_query(select(Categories.id).where(Categories.id==category and Categories.status=="soft_delete")) != []):
        return error_message(400, "Category not found.")
    elif price < 1:
        return error_message(400, "Price must be positive numbers.")
    elif condition != "new" or condition != "used":
        return error_message(400, "Fill condition with only 'new' or 'used'")
    elif description.count("")-1 < 50:
        return error_message(400, f"Description less than 50 characters, add {50 - (description.count('')-1)} characters more.")
    elif run_query(select(Products.name, Products.category_id, Products.condition).where(Products.name==product_name and Products.category_id==category and Products.condition==condition and Products.condition!='soft_delete')) == [{"name": product_name, "category_id": category, "condition": condition}]:
        return error_message(409, f"Product '{product_name}' already exist.")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        run_query(update(Products).values(category_id=category, name=product_name, price=price, condition=condition, images_url=str(images), detail=description, update_at=format_datetime(), update_by=user_name).where(Products.id==product_id and Products.condition!="soft_delete"), True)
        return success_message(200, f"Product '{product_name}' updated.")

@products_bp.route("", methods=["DELETE"])
@decode_auth_token
def delete_product(current_user):
    product_id = request.args.get("product_id", type=str)

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user.")
    elif (run_query(select(Products.id).where(Products.id==product_id and Products.condition!='soft_delete')) == []) or (run_query(select(Products.id).where(Products.id==product_id and Products.condition=='soft_delete')) != []):
        return error_message(400, "Product not found.")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        product_name = run_query(select(Products.name).where(Products.id==product_id))[0]["name"]
        run_query(update(Products).values(condition="soft_delete", update_at=format_datetime(), update_by=user_name).where(Products.id==product_id and Products.condition!="soft_delete"), True)
        return success_message(200, f"Product '{product_name}' deleted.")

@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    # http://127.0.0.1:5000/products/search_image
    body = request.get_json()
    if "image" not in body: return error_message(400, "Can't search image, image is empty")
    image = body["image"]
    query = run_query(f"SELECT DISTINCT category_id FROM products WHERE images_url='{image}'")
    return success_message(200, key="result", data=query)

@products_bp.route("/<id>", methods=["GET"])
def get_product_details(id):
    if [{"id": id}] == run_query(f"SELECT id FROM products WHERE id='{id}'"):
        query = run_query(
                f"""SELECT id, name, size, detail, price, images_url
                    FROM products
                    WHERE id='{id}'
                """
            )
    else: return error_message(404, "Not Found")
    return success_message(200, msg=query)
