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
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import products_bp


# first save image to model Images, then for column images url in model product fill the endpoint image
@products_bp.route("", methods=["POST"])
def create_product():
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
    run_query(f"DELETE FROM products", True)
    run_query(f"INSERT INTO products VALUES ('pid1', 'cid1', 'p123', '100', 'lorem', 'image1', 'used', 'S', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid2', 'cid1', 'p123', '60', 'lorem', 'image2', 'used', 'L', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid3', 'cid1', 'p789', '110', 'lorem', 'image3', 'used', 'M', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid4', 'cid2', 'p789', '500', 'lorem', 'image1', 'used', 'M', '{format_datetime()}', 'admin')", True)
    # http://127.0.0.1:5000/products?category=cid1&price=100&product_name=p123&condition=used&sort_by=price_a_z

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
def update_product():
    pass

@products_bp.route("", methods=["DELETE"])
def delete_product():
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