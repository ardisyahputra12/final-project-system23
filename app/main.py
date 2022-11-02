from flask import Flask
from utils import create_table
from blueprints import products_bp, categories_bp
from universal import universal_bp
from home import home_bp
from authentication import sign_up_bp, sign_in_bp
# from product_list import products_bp, categories_bp
from cart import cart_bp, shipping_price_bp
from profile_page import user_bp, order_bp
from admin_page import orders_bp, sales_bp


def create_app():
    app = Flask(__name__)
    blueprints = [
        universal_bp,
        home_bp,
        sign_up_bp,
        sign_in_bp,
        products_bp,
        categories_bp,
        cart_bp,
        shipping_price_bp,
        user_bp,
        order_bp,
        orders_bp,
        sales_bp
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    create_table()
    return app


app = create_app()
app.run()