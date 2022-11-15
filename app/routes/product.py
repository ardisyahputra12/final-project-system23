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
    pass

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
    run_query(delete(Products), True)
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid1", name="baju", price=60, condition="used", images_url="image1", detail="lorem", create_by='Saya'), True)
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid1", name="baju", price=100, condition="used", images_url="image1", detail="lorem", create_by='Saya'), True)
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid1", name="baju", price=99, condition="used", images_url="image2", detail="lorem", create_by='Saya'), True)
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid2", name="celana", price=110, condition="used", images_url="image2", detail="lorem", create_by='Saya'), True)
    # http://127.0.0.1:5000/products?category=cid1&price=100&product_name=baju&condition=used&sort_by=price_a_z

    if category == None or price == None or product_name == None or condition == None:
        return error_message(400, "Params category, price, product_name, and condition can't empty")
    elif (page != None and page < 1) or (page_size != None and page_size < 1) or (price != None and price < 1):
        return error_message(400, "Params Page, page size, and price must be positive numbers")
    else:
        if page_size==None: page_size=5
        if sort_by == "price_z_a": sort = 'DESC'
        elif sort_by == "price_a_z" or sort_by == None: sort = 'ASC'
        else: return error_message(400, "Params sort_by unknown, please use price_z_a or price_a_z")
        query = run_query(
                f"""SELECT id, images_url, name, price
                    FROM products
                    WHERE category_id='{category}' and price<={price} and name='{product_name}' and condition='{condition}'
                    ORDER BY price {sort}
                    LIMIT {page_size}
                """
            )
        return success_message(200, data=query)

@products_bp.route("", methods=["PUT"])
@decode_auth_token
def update_product(current_user):
    pass

@products_bp.route("", methods=["DELETE"])
@decode_auth_token
def delete_product(current_user):
    pass

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