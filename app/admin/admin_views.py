from flask_restful import Resource, reqparse
from models.models import FoodItem, FoodItems, FoodOrder, FoodOrders


class Foods(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("description", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("price", type=int, required=True,
                        help="This field can not be left bank")

    def post(self):
        """ create a new food item"""
        data = Foods.parser.parse_args()

        name = data["name"]
        description = data["description"]
        price = data["price"]

        food_item = FoodItem(name, description, price)
        FoodItems.append(food_item)
        return {"message": "Food item created successfully"}, 201

    def get(self):
        """ Get all food items"""

        return {"Food items": [fooditem.serialize() for fooditem in FoodItems]}


class SpecificOrder(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("status", type=str, required=True,
                        help="This field can not be left bank")

    def get(self, order_id):
        """ Get a specific order"""
        order = FoodOrder().get_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404
        else:
            return {"order": order.serialize()}

    def put(self, order_id):
        """ Update a specific order"""
        data = SpecificOrder.parser.parse_args()

        status = data["status"]

        order = FoodOrder().get_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404
        else:
            order.status = status
            return {"order": order.serialize()}
