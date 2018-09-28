import unittest
import json

from app import create_app

from db_tests import migrate, drop, create_admin


class TestFoodItem(unittest.TestCase):

    def setUp(self):
        """ setting up testing """

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.create_data = {
            "food_data": {
                "name": "njahindengu",
                "description": "sliced",
                "price": 47
            }
        }
        with self.app.app_context():
            drop()
            migrate()
            create_admin()

    def signup(self):
        """ signup function """
        signup_data = {
            "username": "kimame123",
            "email": "kimame@gmial.com",
            "password": "Kimame1234"
        }
        response = self.client.post(
            "api/v1/auth/signup",
            data=json.dumps(signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        """ login function """
        login_data = {
            "username": "kimame123",
            "password": "Kimame1234"
        }

        response = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login_admin(self):
        """ method to login admin """

        data = {
            "username": "kimamedave",
            "password": "Kindlypass1"
        }

        response = self.client.post(
            "api/v1/auth/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        return response

    def test_login_as_admin(self):
        """ Test to login in admin """

        response = self.login_admin()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.data)[
                         "message"], "successfully logged")

    def get_token(self):
        """get token """
        self.signup()

        response = self.login()

        token = json.loads(response.data).get("token", None)
        return token

    def get_token_as_admin(self):
        """get token """

        response = self.login_admin()

        token = json.loads(response.data).get("token", None)
        return token

    def test_get_token(self):
        """ Test get token """

        self.signup()
        response = self.login()

        self.assertEqual(response.status_code, 200)

        self.assertIn("token", json.loads(response.data))

    def post_food_item(self):
        """ method to post new food item """

        token = self.get_token_as_admin()

        res = self.client.post(
            "/api/v1/fooditems",
            data=json.dumps(self.create_data['food_data']),
            headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )
        return res

    def test_create_food_item(self):
        """ Test create food item """

        response = self.post_food_item()

        self.assertEqual(response.status_code, 201)

        self.assertEqual(json.loads(response.data)[
            "message"], "Food item created successfully")

    def test_invalid_food_name(self):
        """ Test food name  """
        data = {
            "name": "***********1",
            "description": "sliced food",
            "price": 47
        }

        token = self.get_token_as_admin()

        response = self.client.post(
            "api/v1/fooditems",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "foodname must contain alphanumeric"
                         " characters only")

    def test_upadte_food_item(self):
        """ test to update a specific food item """

        token = self.get_token_as_admin()

        self.post_food_item()

        update_data = {
            "name": "njiva",
            "description": "sweet and cool",
            "price": 190
        }

        response = self.client.put(
            "api/v1/fooditems/1",
            data=json.dumps(update_data),
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_food_description(self):
        """ Test food description  """

        data = {
            "name": "ugaliskuma",
            "description": "*****123",
            "price": 47
        }

        token = self.get_token_as_admin()

        response = self.client.post(
            "api/v1/fooditems",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )
        print(response.data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "description must contain alphanumeric"
                         " characters only")

    def test_get_all_fooditems(self):
        """ Test all food items """

        token = self.get_token()

        self.post_food_item()

        response = self.client.get(
            "api/v1/fooditems",
            headers={"Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_customer_post_order(self):
        """ Test for a customer to place an order  """

        token = self.get_token()
        data = {
            "destination": "juja"
        }
        self.post_food_item()

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 201)

    def test_get_specific_orders(self):
        """ Get a specific food order"""
        token = self.get_token()

        data = {
            "destination": "juja"
        }
        self.post_food_item()

        res = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        response = self.client.get(
            "api/v1/fooditems/orders/1",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_food_item(self):
        """ Test to delete a specific food item  """
        token = self.get_token_as_admin()

        self.post_food_item()
        response = self.client.delete(
            "api/v1/fooditems/1",
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.data)[
                         "message"], "item deleted sucessfully")
