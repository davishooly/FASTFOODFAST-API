import os

import click

from app import create_app

from models.models import DataStore, FoodItem, FoodOrder, User

app = create_app(os.getenv("APP_SETTINGS") or "default")


@app.cli.command()
def migrate():
    """ create tables """
    User().create()
    FoodItem().create()
    FoodOrder().create()


@app.cli.command()
def drop():
    """ drop tables if they exist """
    User().drop()
    FoodItem().drop()
    FoodOrder().drop()


# add admin to db
@app.cli.command()
def create_admin():
    """ add admin """
    user = User(username='kimamedave', email='kimdave@gmail.com',
                password='Kindlypass1', is_admin=True)
    user.add()


if __name__ == '__main__':
    app.run()
