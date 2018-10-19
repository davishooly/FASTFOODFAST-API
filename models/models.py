
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2

# local imports
from flask import current_app


class DataStore:
    """ database connection model """

    def __init__(self):
        self.db_host = current_app.config['DB_HOST']
        self.db_username = current_app.config['DB_USERNAME']
        self.db_password = current_app.config['DB_PASSWORD']
        self.db_name = current_app.config['DB_NAME']

        # connect to fastfoodfast database
        self.conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_username,
            password=self.db_password,
            database=self.db_name,
        )
        # open cursor to perfome database operations
        self.cur = self.conn.cursor()

    def create_table(self, schema):
        """ method to create a table """
        self.cur.execute(schema)
        self.save()

    def drop_table(self, name):
        """ method to drop a table """
        self.cur.execute("DROP TABLE IF EXISTS " + name)
        self.save()

    def save(self):
        """ method to save the changes made """
        self.conn.commit()

    def close(self):
        self.cur.close()


class FoodItem(DataStore):

    def __init__(self, name=None, description=None, price=None):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.date = datetime.now().replace(second=0, microsecond=0)

    def create(self):
        """ create table fooditems """
        self.create_table(
            """
            CREATE TABLE fooditems (
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL,
                description TEXT,
                price INTEGER,
                date  TIMESTAMP
            );
            """
        )

    def drop(self):
        """ drop if table exists """
        self.drop_table('fooditems')

    def add(self):
        """ add fooditem to table"""
        SQL = "INSERT INTO fooditems(name, description, price, date) VALUES (%s, %s, %s,%s )"
        data = (self.name, self.description, self.price, self.date)
        self.cur.execute(SQL, data)
        self.save()

    def map_fooditems(self, data):
        """ map food order to an object"""
        fooditem = FoodItem(
            name=data[1], description=data[2], price=data[3])
        fooditem.id = data[0]
        fooditem.date = data[4]
        self = fooditem

        return self

    def serialize(self):
        """ serialize a FoodItem object to a dictionary"""
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            date=str(self.date),
            price=self.price,
        )

    def fetch_by_id(self, _id):
        """ fetch food by id """
        self.cur.execute(
            "SELECT * FROM fooditems where id = %s", (_id, ))
        food_item = self.cur.fetchone()
        self.save()
        self.close()

        if food_item:
            return self.map_fooditems(food_item)
        return None

    def fetch_by_name(self, name):
        """ fetch food by name """
        self.cur.execute("SELECT * FROM fooditems where name = %s", (name,))
        food_item = self.cur.fetchone()

        if food_item:
            return self.map_fooditems(food_item)
        return None

    def delete(self, food_id):
        """ delete food item """

        self.cur.execute(
            "DELETE FROM fooditems WHERE id = %s", (food_id, )
        )
        self.save()
        self.close()

    def update(self, food_id):
        """ update an existing food item """

        self.cur.execute(
            """ UPDATE fooditems SET name =%s, description =%s, price=%s WHERE id = %s """, (
                self.name, self.description, self.price, food_id)
        )
        self.save()
        self.close()

    def fetch_all_fooditems(self):
        """ fetch all food items """
        self.cur.execute("SELECT * FROM fooditems")
        fooditems = self.cur.fetchall()
        self.save()
        self.close()

        if fooditems:
            return [self.map_fooditems(fooditem) for fooditem in fooditems]
        return None


class FoodOrder(DataStore):

    def __init__(self, order_by=None, by_name=None,  destination=None, Quantity=None):
        super().__init__()
        self.order_by = order_by
        self.by_name = by_name
        self.destination = destination
        self.Quantity = Quantity
        self.date = datetime.now().replace(second=0, microsecond=0)
        self.status = "New"

    def create(self):
        """ create table foodorder """
        self.create_table(
            """
            CREATE TABLE foodorder(
                id serial PRIMARY KEY,
                order_by VARCHAR,
                by_name VARCHAR,
                destination VARCHAR,
                Quantity INTEGER,
                date TIMESTAMP,
                status  VARCHAR NOT NULL
            );
            """
        )

    def drop(self):
        """ drop table if exists """

        self.drop_table('foodorder')

    def add(self):
        """ add foodorder to table"""
        SQL = "INSERT INTO foodorder(order_by, by_name, destination, Quantity, date, status) VALUES( %s,%s, %s, %s,%s, %s)"
        data = (self.order_by, self.by_name,
                self.destination, self.Quantity, self.date, self.status)
        self.cur.execute(SQL, data)
        self.save()
        self.close()

    def serialize(self):
        """ serialize a Food Order object to a dictionary"""
        return dict(
            id=self.id,
            orderd_by=self.order_by,
            name=self.by_name,
            status=self.status,
            destination=self.destination,
            Quanity=self.Quantity,
            date=str(self.date),
        )

    def fetch_by_id(self, food_order_id):
        """ fetch food by id """

        self.cur.execute(
            "SELECT * FROM foodorder where id=%s", (food_order_id, ))
        food_order = self.cur.fetchone()
        self.save()
        self.close()

        if food_order:
            return self.map_foodorder(food_order)
        return None

    def fetch_all_orders(self):
        """ fetch all orders """

        self.cur.execute("SELECT *  FROM foodorder ")
        orders = self.cur.fetchall()
        self.save()
        self.close()

        if orders:
            return [self.map_foodorder(order) for order in orders]
        return None

    def orders_by_requester(self, requester):
        """ get all orders made by the requester """

        self.cur.execute(
            """ SELECT *  FROM foodorder WHERE order_by =%s """, (requester, ))

        customer_orders = self.cur.fetchall()
        self.save()
        self.close()

        if customer_orders:
            return [self.map_foodorder(customer_order) for customer_order in customer_orders]
        return None

    def delete(self, food_id):
        """ delete food order """

        self.cur.execute(
            "DELETE FROM foodorder WHERE id = %s", (food_id, )
        )
        self.save()
        self.close()

    def accept_order(self, order_id):
        """ accept order """

        self.cur.execute(
            """ UPDATE foodorder SET status=%s WHERE id = %s""", (
                'Processing', order_id)
        )
        self.save()
        self.close()

    def update_accepted_order_to_completed(self, order_id):
        """ update order as completed """

        self.cur.execute(
            """ UPDATE foodorder SET status=%s WHERE id=%s""", ('complete', order_id))

        self.save()
        self.close()

    def reject_order(self, order_id):
        """ reject an order """

        self.cur.execute(
            """ UPDATE foodorder SET status=%s WHERE id= %s """, (
                'Cancelled', order_id
            )
        )
        self.save()
        self.close()

    def fetch_all_accepted_orders(self):
        """ fetch all accepted orders """

        self.cur.execute(
            " SELECT * FROM foodorder WHERE status = %s", ('Processing',))

        accepted_orders = self.cur.fetchall()
        self.save()
        self.close()

        if accepted_orders:
            return [self.map_foodorder(accepted_order) for accepted_order in accepted_orders]
        return None

    def fetch_all_rejected_orders(self):
        """ fetch all rejected orders """

        self.cur.execute(
            """ SELECT * FROM foodorder WHERE status = %s""", ('Cancelled',))

        rejected_orders = self.cur.fetchall()
        self.save()
        self.close()

        if rejected_orders:
            return [self.map_foodorder(rejected_order) for rejected_order in rejected_orders]
        return None

    def fetch_all_completed_orders(self):
        """ fetch all completed orders """

        self.cur.execute(
            """ SELECT * FROM foodorder WHERE status = %s""", ('complete',))

        completed_orders = self.cur.fetchall()
        print(completed_orders)

        self.save()
        self.close()

        print(completed_orders)

        if completed_orders:
            return [self.map_foodorder(completed_order) for completed_order in completed_orders]
        return None

    def map_foodorder(self, data):
        """ map food order to an object"""
        food_order = FoodOrder(
            order_by=data[1], by_name=data[2], destination=data[3], Quantity=data[4])
        food_order.id = data[0]
        food_order.date = data[5]
        food_order.status = data[6]
        self = food_order

        return self


class User(DataStore):

    def __init__(self,  username=None, email=None, password=None, is_admin=False):
        super().__init__()
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def create(self):
        """ create table users """
        self.create_table(
            """
            CREATE TABLE users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL,
                email  VARCHAR NOT NULL,
                password VARCHAR NOT NULL,
                is_admin BOOLEAN NOT NULL
            );
            """
        )

    def drop(self):
        """ drop table if exists """
        self.drop_table('users')

    def add(self):
        """ add users to table"""
        SQL = "INSERT INTO users(username, email, password, is_admin) VALUES( %s, %s, %s, %s)"
        data = (self.username, self.email, self.password_hash, self.is_admin)
        self.cur.execute(SQL, data)
        self.save()

    def map_user(self, data):
        """ map user to an object"""

        self.id = data[0]
        self.username = data[1]
        self.email = data[2]
        self.password_hash = data[3]
        self.is_admin = data[4]

        return self

    def fetch_by_username(self, username):
        """ fetch user by username """
        self.cur.execute(
            "SELECT * FROM users WHERE username=%s", (username,))
        user = self.cur.fetchone()

        if user:
            return self.map_user(user)
        return None

    def fetch_by_email(self, email):
        """ fetch user by email """
        self.cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = self.cur.fetchone()

        if user:
            return self.map_user(user)
        return None

    def serialize(self):
        """ serialize a user to a dictionary """
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            is_admin=self.is_admin
        )
