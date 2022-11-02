from utils import run_query, error_message, success_message
from blueprints import products_bp, categories_bp
from datetime import datetime
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

# products_bp = Blueprint("products", __name__, url_prefix="/products")
# categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


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
    run_query(f"INSERT INTO products VALUES ('pid1', 'cid1', 'p123', '100', 'lorem', 'S', 'used', 'image1', 'imagesss', '{datetime.now()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid2', 'cid1', 'p123', '60', 'lorem', 'L', 'used', 'image2', 'imagesss', '{datetime.now()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid3', 'cid1', 'p789', '110', 'lorem', 'M', 'used', 'image3', 'imagesss', '{datetime.now()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid4', 'cid2', 'p789', '500', 'lorem', 'M', 'used', 'image1', 'imagesss', '{datetime.now()}', 'admin')", True)
    # http://127.0.0.1:5000/products?category=cid1&price=100&product_name=p123&condition=used&sort_by=price_a_z

    if category == None or price == None or product_name == None or condition == None:
        return error_message("Params category, price, product_name, and condition can't empty", 400)
    elif (page != None and page < 1) or (page_size != None and page_size < 1) or (price != None and price < 1):
        return error_message("Params Page, page size, and price must be positive numbers", 400)
    else:
        if page_size==None: page_size=5
        if sort_by == "price_z_a": sort = 'DESC'
        elif sort_by == "price_a_z" or sort_by == None: sort = 'ASC'
        else: return error_message("Params sort_by unknown, please use price_z_a or price_a_z", 400)
        query = run_query(
                f"""SELECT product_id, product_image, product_name, product_price
                    FROM products
                    WHERE category_id='{category}' and product_price<={price} and product_name='{product_name}' and product_condition='{condition}'
                    ORDER BY product_price {sort}
                    LIMIT {page_size}
                """
            )
        return {
            "data": [
                query
            ],
            "total_rows": len(query),
        }, 200

@categories_bp.route("", methods=["GET"])
def get_category():
    # For testing only
    run_query(f"DELETE FROM categories", True)
    run_query(f"INSERT INTO categories VALUES ('cid1', 'baju', '{datetime.now()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid2', 'celana', '{datetime.now()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid3', 'kaos', '{datetime.now()}', 'admin')", True)
    # http://127.0.0.1:5000/categories

    return {
        "data": [
            run_query(f"SELECT category_id, category_name FROM categories")
        ]
    }, 200

@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    # http://127.0.0.1:5000/products/search_image?image=image1
    body = request.get_json()
    # image = request.args.get("image", type=str)
    if "image" not in body: return error_message("Can't search image, image is empty", 400)
    image = body["image"]

    return {
        "category_id": run_query(f"SELECT DISTINCT category_id FROM products WHERE product_image='{image}'"),
    }