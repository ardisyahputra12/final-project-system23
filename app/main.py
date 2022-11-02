from flask import Flask
from utils import create_table
from routes.universal import universal_bp
from routes.home import home_bp
from routes.auth import sign_up_bp, sign_in_bp
from routes.product import products_bp
from routes.category import categories_bp
from routes.cart import cart_bp, shipping_price_bp
from routes.user import user_bp, sales_bp
from routes.order import orders_bp, order_bp


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