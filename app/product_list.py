from utils import run_query, error_message, success_message
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)

products_bp = Blueprint("products", __name__, url_prefix="/products")
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


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

    if category == None or price == None or product_name == None:
        return {
            "error": "Category, price, and product_name can't empty"
        }, 400
    elif (page != None and page < 1) or (page_size != None and page_size < 1) or (price != None and price < 1):
        return {
            "error": "Page, page size, and price must be positive numbers"
        }, 400
    else:
        if page_size==None: page_size=5
        def query(sort):
            if sort == "Price z_a": sort = 'DESC'
            else: sort = 'ASC'
            return run_query(f"""SELECT product_id, product_image, product_name, product_price
                          FROM products
                          WHERE category_id={category} and product_price<{price} and product_name={product_name} and product_condition={condition}
                          ORDER BY {sort}
                          LIMIT {page_size}
                          """)
        return {
            "data": [
                query(sort_by)
            ],
            "total_rows": len(query(sort_by)),
        }, 200

@categories_bp.route("", methods=["GET"])
def get_category():
    return {
        "data": [
            run_query(f"SELECT category_id, category_name FROM categories")
        ]
    }, 200

@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    if request.args.get("page_size", type=int) != None: page_size = request.args.get("page_size", type=int)
    else: page_size = request.get_json()["page_size"]
    data_query = run_query(f"SELECT product_id, product_image, product_name, product_price FROM products LIMIT {page_size}")
    def category_query(col):
        return run_query(f"SELECT categories.{col} FROM categories INNER JOIN products ON products.category_id=categories.category_id")

    return {
        "data": [
            data_query
        ],
        "category": category_query('category_name'),
        "category_id": category_query('category_id'),
        "total_rows": len(data_query)
    }