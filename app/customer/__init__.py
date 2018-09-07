from flask import Blueprint
from .customer_views import PostOrders, GetOrders, Order

customer_blueprint = Blueprint("customer", __name__)
