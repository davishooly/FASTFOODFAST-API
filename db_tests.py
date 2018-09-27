# module imports
import os

# local imports
from models.models import DataStore, FoodItem, FoodOrder, User

from app import create_app

app = create_app("testing")


def migrate():
    """ create test tables """

    User().create()
    FoodItem().create()
    FoodOrder().create()


def drop():
    """ drop test tables if they exist """

    User().drop()
    FoodItem().drop()
    FoodOrder().drop()
