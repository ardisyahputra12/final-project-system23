from flask import Blueprint

products_bp = Blueprint("products", __name__, url_prefix="/products")
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")