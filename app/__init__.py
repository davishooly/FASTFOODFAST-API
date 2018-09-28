# module imports
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

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

    # Regestering blueprints for my views
    from .admin import admin_blueprint as admin_blp
    admin = Api(admin_blp)
    app.register_blueprint(admin_blp, url_prefix="/api/v1")

    from .auth import auth_blueprint as auth_blp
    auth = Api(auth_blp)
    app.register_blueprint(auth_blp, url_prefix="/api/v1/auth")

    from .customer import customer_blueprint as customer_blp
    customer = Api(customer_blp)
    app.register_blueprint(customer_blp, url_prefix="/api/v1")

    # Routes
    admin.add_resource(Foods, '/fooditems')
    admin.add_resource(SpecificFoodItem, '/fooditems/<int:food_item_id>')
    admin.add_resource(SpecificOrder, '/fooditems/orders/<int:order_id>')
    admin.add_resource(
        AcceptFoodOrders, '/fooditems/orders/<int:order_id>/accept')
    admin.add_resource(AcceptedOrders, '/fooditems/accepted/orders')
    admin.add_resource(
        RejectFoodOrders, '/fooditems/orders/<int:order_id>/reject')
    admin.add_resource(
        RejectedOrders, '/fooditems/rejected/orders')
    admin.add_resource(
        CompleteFoodOrders, '/fooditems/orders/<int:order_id>/complete')
    admin.add_resource(
        CompletedOrders, '/fooditems/completed/orders')
    admin.add_resource(GetOrders, '/fooditems/orders')
    admin.add_resource(OrderHistoryForSpecificUser, '/orders/<username>')

    auth.add_resource(SignUp, '/signup')
    auth.add_resource(Login, '/login')

    customer.add_resource(PostOrders, '/fooditems/<int:food_id>/orders')
    customer.add_resource(Order, '/fooditems/orders/<int:food_order_id>')
    customer.add_resource(CustomersOrderHistory,
                          '/fooditems/orders/orderhistory')

    return app
