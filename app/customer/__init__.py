from flask import Blueprint
from .customer_views import PostOrders, Order, CustomersOrderHistory

customer_blueprint = Blueprint("customer", __name__)
