from flask import Flask
from models import get_engine
import models
import routes


def create_app():
    app = Flask(__name__)
    engine = get_engine()
    blueprints = [
        routes.universal_bp,
        routes.home_bp,
        routes.sign_up_bp,
        routes.sign_in_bp,
        routes.products_bp,
        routes.categories_bp,
        routes.cart_bp,
        routes.shipping_price_bp,
        routes.user_bp,
        routes.order_bp,
        routes.orders_bp,
        routes.sales_bp,
    ]

    models.Base.metadata.create_all(bind=engine)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


create_app()