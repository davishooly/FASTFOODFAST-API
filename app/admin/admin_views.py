from flask_restful import Resource, reqparse
from models.models import FoodItem, FoodItems, FoodOrder, FoodOrders

from flask_jwt_extended import jwt_required

from utils import validators


class Foods(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("description", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("price", type=int, required=True,
                        help="This field can not be left bank")

    @jwt_required
    def post(self):
        """ create a new food item"""
        data = Foods.parser.parse_args()

        name = data["name"]
        description = data["description"]
        price = data["price"]

        validate = validators.Validators()

        if not validate.valid_inputs(name):
            return {"message": "foodname must contain alphanumeric"
                    " characters only"}, 400

        if not validate.valid_inputs(description):
            return {"message": "description must contain alphanumeric"
                    " characters only"}, 400

        # food_item = FoodItem().get_by_name(name)
        #   if food_item:
        #     return {"message": "food item already exists"}, 400

        food_item = FoodItem(name, description, price)
        FoodItems.append(food_item)

        return {"message": "Food item created successfully"}, 201

    @jwt_required
    def get(self):
        """ Get all food items"""

        return {"Food items": [fooditem.serialize() for fooditem in FoodItems]}


class SpecificFoodItem(Resource):

    @jwt_required
    def delete(self, food_item_id):
        """ delete food item """
        food_item = FoodItem().get_by_id(food_item_id)

        if not food_item:
            return {"message": "food item does not exist"}, 404

        FoodItems.remove(food_item)
        return {"message": "item deleted sucessfully"}, 200


class SpecificOrder(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("status", type=str, required=True,
                        help="This field can not be left bank")

    @jwt_required
    def get(self, order_id):
        """ Get a specific order"""
        order = FoodOrder().get_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404
        else:
            return {"order": order.serialize()}

    @jwt_required
    def put(self, order_id):
        """ Update a specific order"""
        data = SpecificOrder.parser.parse_args()

        status = data["status"]

        validate = validators.Validators()

        if not validate.valid_inputs(status):
            return {"message": "status must contain alphanumeric"
                    " characters only"}, 400

        order = FoodOrder().get_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404
        else:
            order.status = status
            return {"order": order.serialize()}
