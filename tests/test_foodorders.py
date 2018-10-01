import unittest
import json

from app import create_app

from db_tests import migrate, drop, create_admin


class TestFoodOrder(unittest.TestCase):

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

    def get_token_as_admin(self):
        """get token """

        response = self.login_admin()

        token = json.loads(response.data).get("token", None)
        return token

    def get_token(self):
        """get token """

        self.signup()

        response = self.login()

        token = json.loads(response.data).get("token", None)
        return token

        self.assertEqual(json.loads(res.data)[
                         'message'], "Order placed successfully")

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

    def post_food_order(self):
        """ method to post new food item """

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

        return res

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

    def test_accept_order(self):
        """ test to accept order """

        token = self.get_token_as_admin()

        self.post_food_order()

        response = self.client.put(
            "api/v1/fooditems/orders/1/accept",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_accept_already_accepted_order(self):
        """ test accept already accepted order """

        token = self.get_token_as_admin()

        self.post_food_order()

        res = self.client.put(
            "api/v1/fooditems/orders/1/accept",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        response = self.client.put(
            "api/v1/fooditems/orders/1/accept",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 403)

    def test_get_all_accepted_food_order(self):
        """ test get all accept food orders """

        token = self.get_token_as_admin()

        self.post_food_order()

        resp = self.client.put(
            "api/v1/fooditems/orders/1/accept",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        response = self.client.get(
            "api/v1/fooditems/accepted/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_accepted_food_order_does_not_exist(self):
        """ test accepted food orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v1/fooditems/accepted/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_reject_order(self):
        """ test to accept order """

        token = self.get_token_as_admin()

        self.post_food_order()

        response = self.client.put(
            "api/v1/fooditems/orders/1/reject",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_reject_already_rejected_order(self):
        """ test accept already accepted order """

        token = self.get_token_as_admin()

        self.post_food_order()

        res = self.client.put(
            "api/v1/fooditems/orders/1/reject",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        response = self.client.put(
            "api/v1/fooditems/orders/1/reject",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 403)

    def test_get_all_rejected_food_order(self):
        """ test get all rejected food orders """

        token = self.get_token_as_admin()

        self.post_food_order()

        resp = self.client.put(
            "api/v1/fooditems/orders/1/reject",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        response = self.client.get(
            "api/v1/fooditems/rejected/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_rejected_food_order_does_not_exist(self):
        """ test rejected food orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v1/fooditems/rejected/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_complete_food_order(self):
        """ test complete an order """

        token = self.get_token_as_admin()

        self.post_food_order()

        resp = self.client.put(
            "api/v1/fooditems/orders/1/accept",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        response = self.client.put(
            "api/v1/fooditems/orders/1/complete",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    # def test_get_completed_orders(self):
    #     """ test rejected food orders does not exist """

    #     self.post_food_order()

    #     token = self.get_token_as_admin()

    #     res = self.client.put(
    #         "api/v1/fooditems/orders/1/complete",
    #         headers={'content-type': 'application/json',
    #                  'Authorization': f'Bearer {token}'}
    #     )

    #     response = self.client.get(
    #         "api/v1/fooditems/completed/orders",
    #         headers={'content-type': 'application/json',
    #                  'Authorization': f'Bearer {token}'}
    #     )

    #     self.assertEqual(response.status_code, 200)

    # def test_completed_food_orders_does_not_exist(self):
    #     """ test completed food orders does not exist """

    #     token = self.get_token_as_admin()

    #     response = self.client.get(
    #         "api/v1/fooditems/completed/orders",
    #         headers={'content-type': 'application/json',
    #                  'Authorization': f'Bearer {token}'}
    #     )

    #     self.assertEqual(response.status_code, 404)

    def test_get_customer_order_history(self):
        """ get all customers order history """

        token = self.get_token()

        self.post_food_order()

        response = self.client.get(
            "api/v1/fooditems/orders/orderhistory",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_user_order_history_doesnot_exist(self):
        """ test user order history does not exist """

        token = self.get_token()

        response = self.client.get(
            "api/v1/fooditems/orders/orderhistory",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_get_specific_user_order_history(self):
        """ test get order history of a specific user """

        token = self.get_token_as_admin()

        self.post_food_order()

        response = self.client.get(
            "api/v1/orders/kimame123",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_specific_user_order_history_does_not_exist(self):
        """ test order history of a specific user does not exist"""

        token = self.get_token_as_admin()

        self.post_food_order()

        response = self.client.get(
            "api/v1/orders/kimame",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_food_order_as_user(self):
        """ test for customer to delete his/her food order """

        token = self.get_token()

        res = self.post_food_order()

        response = self.client.delete(
            "api/v1/fooditems/orders/1",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
