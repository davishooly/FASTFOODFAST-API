import unittest
import json

from app import create_app

from db_tests import migrate, drop


class TestFoodOrder(unittest.TestCase):

    def setUp(self):
        """ setting up testing """

        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            drop()
            migrate()

    def signup(self):
        """ signup function """

        signup_data = {
            "username": "kimame123",
            "email": "kimame@gmial.com",
            "password": "Kimame1234",
            "is_admin": False
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

    def get_token(self):
        """get token """

        self.signup()

        response = self.login()

        token = json.loads(response.data).get("token", None)
        return token

        self.assertEqual(json.loads(res.data)[
                         'message'], "Order placed successfully")

    def test_fooditem_does_not_exist(self):
        """ Test food item does not exist """

        token = self.get_token()

        data = {
            "destination": "juja"
        }

        response = self.client.post(
            "/api/v1/fooditems/100/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertEqual(json.loads(response.data)[
                         'message'], "Food item does not exist")

    def test_invalid_destination(self):
        """ Test for an invalid destination """

        token = self.get_token()

        data = {
            "destination": "********"
        }

        response = self.client.post(
            "/api/v1/fooditems/1/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         'message'], "enter valid destination")

    def test_food_order_does_not_exist(self):
        """ Test food order does not exist """
        token = self.get_token()

        response = self.client.get(
            "api/v1/fooditems/orders/100",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertEqual(json.loads(response.data)[
                         'message'], "order does not exist")

    def test_if_status_is_valid(self):
        """ Test if status is valid """

        token = self.get_token()

        status_data = {
            "status": "*****"
        }

        response = self.client.put(
            "api/v1/fooditems/orders/1",
            data=json.dumps(status_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         'message'], "status must contain alphanumeric"
                         " characters only")
