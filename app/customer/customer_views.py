# module imports
from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required

# local imports
from utils import validators
from models.models import FoodOrder, FoodOrders, FoodItem


class PostOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("destination", type=str, required=True,
                        help="This field can not be left bank")

    @jwt_required
    def post(self, food_id):
        """post an order"""

        data = PostOrders.parser.parse_args()

        destination = data["destination"]

        validate = validators.Validators()

        if not validate.valid_inputs(destination):
            return {"message": "enter valid destination"}, 400

        food_item = FoodItem().get_by_id(food_id)

        if not food_item:
            return {"message": "Food item does not exist"}, 404

        food_order = FoodOrder(food_item.name, destination)

        FoodOrders.append(food_order)

        return {"message": "Order placed successfully"}, 201


class GetOrders(Resource):

    @jwt_required
    def get(self):
        """get a list of all orders"""
        print(FoodOrders)
        return {"List orders": [food_order.serialize()
                                for food_order in FoodOrders]}


class Order(Resource):

    def delete(self, food_order_id):
        """ delete food order """
        food_order = FoodOrder().get_by_id(food_order_id)

        if not food_order:
            return {"message": "food order does not exist"}, 404
        else:
            FoodOrders.remove(food_order)
            return {"message": "order deleted sucessfully"}, 200
