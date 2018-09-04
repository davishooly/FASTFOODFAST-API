from flask_restful import Resource, reqparse

from models.models import FoodOrder, FoodOrders, FoodItem


class PostOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("destination", type=str, required=True,
                        help="This field can not be left bank")

    def post(self, food_id):
        data = PostOrders.parser.parse_args()
        destination = data["destination"]

        food_item = FoodItem().get_by_id(food_id)

        if not food_item:
            return {"message": "Food item does not exist"}, 404

        food_order = FoodOrder(food_item.name, destination)

        FoodOrders.append(food_order)

        return {"message": "Order placed successfully"}, 201


class GetOrders(Resource):

    def get(self):
        """get a list of all orders"""
        return {"List orders": [food_order.serialize()
                                for food_order in FoodOrders]}
