from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

FoodItems = []
FoodOrders = []
Users = []


class FoodItem:

    food_item_id = 1

    def __init__(self, name=None, description=None, price=None):
        self.name = name
        self.description = description
        self.price = price
        self.date = datetime.now().replace(second=0, microsecond=0)
        self.id = FoodItem.food_item_id

        FoodItem.food_item_id += 1

    def serialize(self):
        """ serialize a FoodItem object to a dictionary"""
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            date=str(self.date),
            price=self.price,
        )

    def get_by_id(self, _id):
        """get food by id """
        for food_item in FoodItems:
            if food_item.id == _id:
                return food_item

    def get_by_name(self, name):
        """ get food by name """
        for food_item in FoodItems:
            if food_item.name == name:
                return food_item


class FoodOrder:

    food_order_id = 1

    def __init__(self, name=None,  destinantion=None):
        self.destinantion = destinantion
        self.name = name
        self.date = datetime.now().replace(second=0, microsecond=0)
        self.status = "PENDING"
        self._id = FoodOrder.food_order_id

        FoodOrder.food_order_id += 1

    def serialize(self):
        """ serialize a Food Order object to a dictionary"""
        return dict(
            id=self._id,
            name=self.name,
            status=self.status,
            destinantion=self.destinantion,
            date=str(self.date),
        )

    def get_by_id(self, _d):
        for order in FoodOrders:
            if order._id == _d:
                return order


class User:

    user_id = 1

    def __init__(self,  username=None, email=None, password=None,
                 is_admin=None):

        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.id = User.user_id

        User.user_id += 1

    def get_by_username(self, username):
        for user in Users:
            if user.username == username:
                return user

    def get_by_email(self, email):
        for user in Users:
            if user.email == email:
                return user
