import unittest
import json

from .base_test import BaseTest


class TestFoodOrder(BaseTest):

    def test_fooditem_does_not_exist(self):
        """ Test food item does not exist """

        token = self.get_token_as_user()

        response = self.client.post(
            "/api/v2/user/100/orders",
            data=json.dumps(self.post_order_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_invalid_destination(self):
        """ Test for an invalid destination """

        token = self.get_token_as_user()
        response = self.client.post(
            "/api/v2/users/1/orders",
            data=json.dumps(self.invalid_destination_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 400)


    def test_food_order_does_not_exist(self):
        """ Test food order does not exist """
        token = self.get_token_as_user()

        response = self.client.get(
            "api/v2/menu/orders/100",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_accept_order(self):
        """ test to accept order """

        token = self.get_token_as_admin()

        self.post_food_order()

        response = self.accept_order()

        self.assertEqual(response.status_code, 200)

    def test_accept_already_accepted_order(self):
        """ test accept already accepted order """

        token = self.get_token_as_admin()

        self.post_food_order()

        self.accept_order()

        response = self.accept_order()

        self.assertEqual(response.status_code, 403)

    def test_get_all_accepted_food_order(self):
        """ test get all accept food orders """

        token = self.get_token_as_admin()

        self.post_food_order()

        self.accept_order()

        response = self.client.get(
            "api/v2/accepted/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_accepted_food_order_does_not_exist(self):
        """ test accepted food orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v2/accepted/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_reject_order(self):
        """ test to accept order """

        token = self.get_token_as_admin()

        self.post_food_order()

        response = self.client.put(
            "api/v2/orders/1/reject",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_reject_already_rejected_order(self):
        """ test accept already accepted order """

        token = self.get_token_as_admin()

        self.post_food_order()

        self.reject_order()

        response = self.reject_order()

        self.assertEqual(response.status_code, 403)

    def test_get_all_rejected_food_order(self):
        """ test get all rejected food orders """

        token = self.get_token_as_admin()

        self.post_food_order()

        self.reject_order()

        response = self.client.get(
            "api/v2/rejected/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_rejected_food_order_does_not_exist(self):
        """ test rejected food orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v2/rejected/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_complete_food_order(self):
        """ test complete an order """

        token = self.get_token_as_admin()

        self.post_food_order()

        self.accept_order()
        response = self.complete_order()

        self.assertEqual(response.status_code, 200)

    def test_get_completed_orders(self):
        """ test rejected food orders does not exist """

        token = self.get_token_as_admin()
        self.post_food_order()

        self.accept_order()
        self.complete_order()

        response = self.client.get(
            "api/v2/completed/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_completed_food_orders_does_not_exist(self):
        """ test completed food orders does not exist """

        token = self.get_token_as_admin()

        response = self.client.get(
            "api/v2/completed/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_user_order_history_doesnot_exist(self):
        """ test user order history does not exist """

        token = self.get_token_as_user()

        response = self.client.get(
            "api/v2/users/orders",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_specific_user_order_history_does_not_exist(self):
        """ test order history of a specific user does not exist"""

        token = self.get_token_as_admin()

        self.post_food_order()

        response = self.client.get(
            "api/v2/orders/kimame",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_food_order_as_user(self):
        """ test for customer to delete his/her food order """

        token = self.get_token_as_user()

        res = self.post_food_order()

        response = self.client.delete(
            "api/v2/orders/1",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)
