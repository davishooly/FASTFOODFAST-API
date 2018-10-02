import unittest
import json

from .base_test import BaseTest

class TestFoodItem(BaseTest):

    def test_get_token(self):
        """ Test get token """

        self.signup()
        response = self.login()

        self.assertEqual(response.status_code, 200)

        self.assertIn("token", json.loads(response.data))

    def test_create_food_item(self):
        """ Test create food item """

        token = self.get_token_as_admin()

        response = self.post_food_item()

        self.assertEqual(response.status_code, 201)

        self.assertEqual(json.loads(response.data)[
            "message"], "Food item created successfully")

    def test_invalid_food_name(self):
        """ Test food name  """
        token = self.get_token_as_admin()

        response = self.client.post(
            "api/v2/menu",
            data=json.dumps(self.invalid_food_name),
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "foodname must contain alphanumeric"
                         " characters only")

    def test_update_food_item(self):
        """ test to update a specific food item """

        token = self.get_token_as_admin()

        self.post_food_item()
        response = self.client.put(
            "api/v2/menu/1",
            data=json.dumps(self.update_data),
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_update_non_existing_food_item(self):
        """ test to update non existing food item """

        token = self.get_token_as_admin()

        response = self.client.put(
            "api/v2/menu/1",
            data=json.dumps(self.update_data),
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_invalid_food_description(self):
        """ Test food description  """

        token = self.get_token_as_admin()

        response = self.client.post(
            "api/v2/menu",
            data=json.dumps(self.invalid_description_data),
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(json.loads(response.data)[
                         "message"], "description must contain alphanumeric"
                         " characters only")

    def test_get_all_fooditems(self):
        """ Test all food items """

        self.post_food_item()

        response = self.client.get(
            "api/v2/menu"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_all_fooditems_as_admin(self):
        """ Test all food items """

        token = self.get_token_as_admin()

        self.post_food_item()

        response = self.client.get(
            "api/v2/menu",
            headers={"Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_customer_post_order(self):
        """ Test for a customer to place an order  """

        token = self.get_token_as_user()

        data = {
            "destination": "juja"
        }
        self.post_food_item()

        res = self.client.post(
            "/api/v2/users/1/orders",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 201)

    def test_get_specific_orders(self):
        """ Get a specific food order"""
        token = self.get_token_as_user()

        self.post_food_item()

        res = self.client.post(
            "/api/v2/users/1/orders",
            data=json.dumps(self.post_order_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        response = self.client.get(
            "api/v2/orders/1",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_food_item_as_admin(self):
        """ Test to delete a specific food item  """
        token = self.get_token_as_admin()

        self.post_food_item()
        response = self.client.delete(
            "api/v2/menu/1",
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.data)[
                         "message"], "item deleted sucessfully")

    def test_delete_non_existing_food_item_as_admin(self):
        """ Test to delete non existing food item  """
        token = self.get_token_as_admin()

        response = self.client.delete(
            "api/v2/menu/1",
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertEqual(json.loads(response.data)[
                         "message"], "food item does not exist")
