# module imports
from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_restful import Api

from swagger_ui.swagger_ui import get_swaggerui_blueprint

# local imports
from instance.config import app_config
from .admin.admin_views import Foods, SpecificOrder, SpecificFoodItem, AcceptFoodOrders, AcceptedOrders, RejectFoodOrders, RejectedOrders, CompletedOrders, CompleteFoodOrders, GetOrders, OrderHistoryForSpecificUser
from .customer.customer_views import PostOrders, Order, CustomersOrderHistory

from .auth.auth_views import SignUp, Login


jwt = JWTManager()

# application factory


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')

    jwt.init_app(app)

    swagger_url = "https://fasty-v2.herokuapp.com/api/v2/doc"
    api_url = "swagger.yml"

    swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url)

    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    # Regestering blueprints for my views
    from .admin import admin_blueprint as admin_blp
    admin = Api(admin_blp)
    app.register_blueprint(admin_blp, url_prefix="/api/v2")

    from .auth import auth_blueprint as auth_blp
    auth = Api(auth_blp)
    app.register_blueprint(auth_blp, url_prefix="/api/v2")

    from .customer import customer_blueprint as customer_blp
    customer = Api(customer_blp)
    app.register_blueprint(customer_blp, url_prefix="/api/v2")

    # Routes

    admin.add_resource(Foods, '/menu')
    admin.add_resource(SpecificFoodItem, '/menu/<int:food_item_id>')
    admin.add_resource(SpecificOrder, '/orders/<int:order_id>')
    admin.add_resource(
        AcceptFoodOrders, '/orders/<int:order_id>/accept')
    admin.add_resource(AcceptedOrders, '/accepted/orders')
    admin.add_resource(
        RejectFoodOrders, '/orders/<int:order_id>/reject')
    admin.add_resource(
        RejectedOrders, '/rejected/orders')
    admin.add_resource(
        CompleteFoodOrders, '/orders/<int:order_id>/complete')
    admin.add_resource(
        CompletedOrders, '/completed/orders')
    admin.add_resource(GetOrders, '/orders')
    admin.add_resource(OrderHistoryForSpecificUser, '/orders/<username>')

    auth.add_resource(SignUp, '/auth/signup')
    auth.add_resource(Login, '/auth/login')

    customer.add_resource(PostOrders, '/users/<int:food_id>/orders')
    customer.add_resource(Order, '/orders/<int:food_order_id>')
    customer.add_resource(CustomersOrderHistory,
                          '/users/orders')

    return app
