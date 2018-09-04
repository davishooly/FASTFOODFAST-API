from datetime import datetime


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
            _id=self.id,
            name=self.name,
            description=self.description,
            date=str(self.date),
            price=self.price,
        )


FoodItems = []
