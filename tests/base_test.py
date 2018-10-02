import unittest
import json

from app import create_app

from db_tests import migrate, drop, create_admin


class BaseTest(unittest.TestCase):
    def setUp(self):
        """ setting up testing """

        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            drop()
            migrate()
            create_admin()

        self.create_data = {
            "food_data": {
                "name": "njahindengu",
                "description": "sliced",
                "price": 47
            }
        }
        self.user_signup_data = {
            "username": "kimame123",
            "email": "kimame@gmial.com",
            "password": "Kimame1234"
        }
        self.user_login_data = {
            "username": "kimame123",
            "password": "Kimame1234"
        }
        self.admin_login_data = {
            "username": "kimamedave",
            "password": "Kindlypass1"
        }
        self.post_order_data = {
            "destination": "juja"
        }
        self.invalid_description_data = {
            "name": "ugaliskuma",
            "description": "*****123",
            "price": 47
        }
        self.update_data = {
            "name": "njiva",
            "description": "sweet and cool",
            "price": 190
        }
        self.invalid_food_name = {
            "name": "***********1",
            "description": "sliced food",
            "price": 47
        }

        self.incorects_pass_data = {
            "username": "kimame123",
            "password": "Kimame123"
        }
        self.email_already_exists_data = {
            "username": "daviskk",
            "email": "kimame@gmial.com",
            "password": "Kwemoi12"
        }
        self.existing_usernme_data = {
            "username": "kimame123",
            "email": "kwemoi@gmial.com",
            "password": "Kwemoi12"
        }
        self.invalid_password_data = {
            "username": "mwanzia",
            "email": "mwanzia@gmail.com",
            "password": "aimame123"
        }

        self.invalid_email_data = {
            "username": "daviskk",
            "email": "davis",
            "password": "kimame123",
            "is_admin": 1
        }
        self.invalid_username_data = {
            "username": "*****1",
            "email": "davis@gmail.com",
            "password": "kimame123",
            "is_admin": 1
        }
        self.user_doest_not_exist_data = {
            "username": "kimame",
            "password": "Kimame123"
        }

        self.invalid_destination_data = {
            "destination": "********"
        }

    def post_food_order(self):
        """ method to post new food item """

        token = self.get_token_as_admin()

        self.post_food_item()

        res = self.client.post(
            "/api/v2/users/1/orders",
            data=json.dumps(self.post_order_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        return res

    def post_food_item(self):
        """ method to post new food item """

        token = self.get_token_as_admin()

        res = self.client.post(
            "/api/v2/menu",
            data=json.dumps(self.create_data['food_data']),
            headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )
        return res

    def signup(self):
        """ user signup function """
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.user_signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        """ login function """
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.user_login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login_admin(self):
        """ method to login admin """
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.admin_login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def get_token_as_user(self):
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

    def complete_order(self):
        """ complete an order """

        token = self.get_token_as_admin()

        res = self.client.put(
            "api/v2/orders/1/complete",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res

    def accept_order(self):
        """ accept an order """
        token = self.get_token_as_admin()

        res = self.client.put(
            "api/v2/orders/1/accept",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res

    def reject_order(self):
        """ reject an order """
        token = self.get_token_as_admin()

        res = self.client.put(
            "api/v2/orders/1/reject",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        return res
