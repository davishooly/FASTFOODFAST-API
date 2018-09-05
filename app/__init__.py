from flask import Flask
from flask_restful import Api
from instance.config import app_config
from .admin.admin_views import Foods, SpecificOrder
from .customer.customer_views import PostOrders, GetOrders

# chop config files


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')

    from .admin import admin_blueprint as admin_blp
    admin = Api(admin_blp)
    app.register_blueprint(admin_blp, url_prefix="/api/v1")

    from .customer import customer_blueprint as customer_blp
    customer = Api(customer_blp)
    app.register_blueprint(customer_blp, url_prefix="/api/v1")

    admin.add_resource(Foods, '/fooditems')
    admin.add_resource(SpecificOrder, '/fooditems/orders/<int:order_id>')

    customer.add_resource(PostOrders, '/fooditems/<int:food_id>/orders')
    customer.add_resource(GetOrders, '/fooditems/orders')

    return app
