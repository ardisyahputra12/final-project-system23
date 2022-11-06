import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from utils import (
    run_query,
    error_message,
    success_message,
    format_datetime,
)
from models.banner import Banner
from models.product_images import Product_images
from models.category import Categories
from . import home_bp


@home_bp.route("/banner", methods=["GET"])
def get_image():
    req = request.args
    product_id = req.get("product")
    
    # For testing only
    run_query(f"DELETE FROM categories", True)
    run_query(f"INSERT INTO categories VALUES ('cid1', 'baju', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid2', 'celana', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid3', 'kaos', '{format_datetime()}', 'admin')", True)
    
    run_query(f"DELETE FROM products", True)
    run_query(f"INSERT INTO products VALUES ('pid1', 'cid1', 'p123', '100', 'lorem', 'S', 'used', 'image1', 'imagesss', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid2', 'cid1', 'p123', '60', 'lorem', 'L', 'used', 'image2', 'imagesss', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid3', 'cid1', 'p789', '110', 'lorem', 'M', 'used', 'image3', 'imagesss', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid4', 'cid2', 'p789', '500', 'lorem', 'M', 'used', 'image1', 'imagesss', '{format_datetime()}', 'admin')", True)
    
    
    if product_id == None:
        query = run_query(f"SELECT id, image, detail FROM products")
    else:
        query = run_query(f"SELECT id, image, detail FROM products where id='{product_id}'")
    if query == []:
        return "<h1>Image Not Found</h1>"
    
    return {
        "data": [
            query
        ]
    }, 200

@home_bp.route("/category", methods=["GET"])
def get_category():
    req = request.args
    category = req.get("category")
    product = req.get("product")
    
    
    # For testing only
    run_query(f"DELETE FROM categories", True)
    run_query(f"INSERT INTO categories VALUES ('cid1', 'baju', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid2', 'celana', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO categories VALUES ('cid3', 'kaos', '{format_datetime()}', 'admin')", True)
    
    run_query(f"DELETE FROM products", True)
    run_query(f"INSERT INTO products VALUES ('pid1', 'cid1', 'p123', '100', 'lorem', 'S', 'used', 'image1', 'imagesss', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid2', 'cid1', 'p123', '60', 'lorem', 'L', 'used', 'image2', 'imagesss', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid3', 'cid1', 'p789', '110', 'lorem', 'M', 'used', 'image3', 'imagesss', '{format_datetime()}', 'admin')", True)
    run_query(f"INSERT INTO products VALUES ('pid4', 'cid2', 'p789', '500', 'lorem', 'M', 'used', 'image1', 'imagesss', '{format_datetime()}', 'admin')", True)
    
    if product == None:
        return "category can't be empty"
    else:
        query = run_query(f"select p.id,p.image,c.name from products p join categories c on p.category_id = c.id where p.id = '{product}'")
    return {
        "data": [
            query
        ]
    },200