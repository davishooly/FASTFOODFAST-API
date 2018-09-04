from datetime import datetime

FoodItems = []
FoodOrders = []


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
        for food_item in FoodItems:
            if food_item.id == _id:
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
