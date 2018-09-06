from flask_restful import Resource, reqparse

from models.models import FoodOrder, FoodOrders, FoodItem

from flask_jwt_extended import jwt_required

from utils import validators


class PostOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("destination", type=str, required=True,
                        help="This field can not be left bank")

    @jwt_required
    def post(self, food_id):
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
