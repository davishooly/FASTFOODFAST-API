# module imports
from flask_restful import Resource, reqparse

from functools import wraps

from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from models.models import FoodItem, FoodOrder, User

from utils import validators


def admin_only(f):
    ''' Restrict access if not admin '''
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        user = User().fetch_by_username(get_jwt_identity())

        if not user.is_admin:
            return {'message': 'Your cannot access this level'}, 401
        return f(*args, **kwargs)
    return wrapper_function


class Foods(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("description", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("price", type=int, required=True,
                        help="This field can not be left bank")

    @jwt_required
    @admin_only
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

        food_item = FoodItem().fetch_by_name(name)

        if food_item:
            return {"message": "food item already exists"}, 400

        food_item = FoodItem(name, description, price)
        food_item.add()

        return {"message": "Food item created successfully"}, 201

    @jwt_required
    def get(self):
        """ Get all food items"""
        fooditems = FoodItem().fetch_all_fooditems()

        if not fooditems:
            return {"message": "There are no fooditems for now "}, 404

        return {"Food items": [fooditem.serialize() for fooditem in fooditems]}, 200


class SpecificFoodItem(Resource):

    @jwt_required
    @admin_only
    def delete(self, food_item_id):
        """ delete food item """
        food_item = FoodItem().fetch_by_id(food_item_id)

        if not food_item:
            return {"message": "food item does not exist"}, 404

        FoodItem().delete(food_item_id)
        return {"message": "item deleted sucessfully"}, 200

    @jwt_required
    def put(self, food_item_id):
        """ update a food item """
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

        if FoodItem().fetch_by_id(food_item_id):
            food_item = FoodItem(name, description, price)
            food_item.update(food_item_id)
            return {"message": "food item update sucessfully"}, 200

        return {"message": "food item does not exist"}, 404


class GetOrders(Resource):

    @jwt_required
    @admin_only
    def get(self):
        """get a list of all orders"""
        orders = FoodOrder().fetch_all_orders()

        if orders:
            return {"message": [order.serialize() for order in orders]}, 200
        return {"message": "no orders placed"}, 404


class SpecificOrder(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("status", type=str, required=True,
                        help="This field can not be left bank")

    @jwt_required
    def get(self, order_id):
        """ Get a specific order"""
        order = FoodOrder().fetch_by_id(order_id)

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

        order = FoodOrder().fetch_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404
        else:
            order.status = status
            return {"order": order.serialize()}


class AcceptFoodOrders(Resource):

    @jwt_required
    @admin_only
    def put(self, order_id):
        """ Update status of a specific order to accepted"""

        order = FoodOrder().fetch_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404

        if order.status != 'PENDING':
            return {'message': 'order already {}'.format(order.status)}

        FoodOrder().accept_order(order_id)
        print(order.status)
        return{'message': 'order accepted sucessfully'}, 200


class AcceptedOrders(Resource):

    @jwt_required
    @admin_only
    def get(self):
        """ get all accepted food orders """

        accepted_orders = FoodOrder().fetch_all_accepted_orders()

        if not accepted_orders:
            return {"message": "no accepted orders currently"}, 404

        return {"orders": [accepted_order.serialize() for accepted_order in accepted_orders]}, 200


class RejectFoodOrders(Resource):

    @jwt_required
    @admin_only
    def put(self, order_id):
        """ update status of a specific order to decline """
        pass

        order = FoodOrder().fetch_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404

        if order.status != 'PENDING' and order.status != 'accepted':
            return {"message": "order already {}".format(order.status)}, 403

        FoodOrder().reject_order(order_id)
        return {"messge": "order rejected sucessfully"}, 200


class RejectedOrders(Resource):

    @jwt_required
    @admin_only
    def get(self):
        """ get all rejected food orders """

        rejected_orders = FoodOrder().fetch_all_rejected_orders()

        if not rejected_orders:
            return {"message": "no rejected orders currently"}, 404

        return {"orders": [rejected_order.serialize() for rejected_order in rejected_orders]}, 200


class CompleteFoodOrders(Resource):

    @jwt_required
    @admin_only
    def put(self, order_id):
        """ update status of a specific order to completed """
        pass

        order = FoodOrder().fetch_by_id(order_id)

        if not order:
            return {"message": "order does not exist"}, 404

        if order.status == 'completed':
            return {"message": "order already {}".format(order.status)}, 403

        if order.status == 'rejected':
            return {"messge": "rejected order cannot be completed"}, 403

        if order.status == 'PENDING':
            return {"message": "accept order fast before completing the order"}, 403

        FoodOrder().update_accepted_order_to_completed(order_id)
        return {"messge": "order completed sucessfully"}, 200


class CompletedOrders(Resource):

    @jwt_required
    @admin_only
    def get(self):
        """ get all completed food orders """

        completed_orders = FoodOrder().fetch_all_completed_orders()

        if not completed_orders:
            return {"message": "no completed orders currently"}, 404

        return {"orders": [completed_order.serialize() for completed_order in completed_orders]}, 200


class OrderHistoryForSpecificUser(Resource):
    @jwt_required
    def get(self, username):
        """ get order history of a specific user """

        user = User().fetch_by_username(username)

        if not user:
            return {"message": "User does not exist"}, 404

        user_orders = FoodOrder().orders_by_requester(user.username)
        return {"message": [order.serialize() for order in user_orders]}, 200
