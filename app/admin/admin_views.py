from flask_restful import Resource, reqparse
from models.models import FoodItem, FoodItems


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
