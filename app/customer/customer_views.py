# Module imports
from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from models.models import FoodOrder, FoodItem, User

from utils import validators


class PostOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("destination", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("Quantity", type=int, required=True,
                        help="Quantity must be an integer")

    @jwt_required
    def post(self, food_id):
        data = PostOrders.parser.parse_args()

        destination = data["destination"]
        quantity = data["Quantity"]

        validate = validators.Validators()

        if not validate.valid_inputs(destination):
            return {"message": "enter valid destination"}, 400

        food_item = FoodItem().fetch_by_id(food_id)

        current_customer = get_jwt_identity()

        if not food_item:
            return {"message": "Food item does not exist"}, 404

        food_order = FoodOrder(
            current_customer["username"], food_item.name, destination, quantity)

        food_order.add()

        return {"message": "Order placed successfully"}, 201


class Order(Resource):

    def delete(self, food_order_id):
        """ delete food order """
        food_order = FoodOrder().fetch_by_id(food_order_id)

        if not food_order:
            return {"message": "food order does not exist"}, 404

        food_order.delete(food_order_id)
        return {"message": "order deleted sucessfully"}, 200


class CustomersOrderHistory(Resource):

    @jwt_required
    def get(self):
        """ get customers order history """

        current_customer = get_jwt_identity()

        customer_orders = FoodOrder().orders_by_requester(
            current_customer['username'])

        if customer_orders:
            return {"order history": [customer_order.serialize() for customer_order in customer_orders]}, 200
        return {"message": "order history empty"}, 404
