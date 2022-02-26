import requests
import unittest
import allure
import os

from dotenv import load_dotenv

from authentication.auth_token import BearerAuth


class AirportApiTest(unittest.TestCase):
    # load env variables
    load_dotenv()

    @classmethod
    def setUpClass(cls):
        """Runs before each test case"""
        cls.BASE_URL = os.environ.get("BASE_URL")
        cls.AIRPORT_API_KEY = os.environ.get("API_TOKEN")

    @allure.feature('Get Airports')
    def test_get_airports(self):
        """Returns all airports, limited to 30 per page"""
        url = f'{self.BASE_URL}/airports'
        response = requests.get(url)
        response_body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(len(response_body["data"]), 30)

    @allure.feature('Calculate distance between airports')
    def test_calculate_distance_between_airports(self):
        url = f'{self.BASE_URL}/airports/distance'
        payload = {"from": "KIX", "to": "SFO"}

        response = requests.post(url, data=payload)
        response_body = response.json()

        self.assertEqual(response.status_code, 200)

        attributes = response_body["data"]["attributes"]

        # assert attributes.keys() >= {'kilometers', 'miles', 'nautical_miles'}
        self.assertTrue(all(key in attributes for key in ('kilometers', 'miles', 'nautical_miles')))
        self.assertEqual(attributes["kilometers"], 8692.066508240026)
        self.assertEqual(attributes["miles"], 5397.239853492001)
        self.assertEqual(attributes["nautical_miles"], 4690.070954910584)

    @allure.feature('Endpoint which requires authentication')
    def test_requires_authentication(self):
        url = f'{self.BASE_URL}/favorites'
        payload = {"airport_id": 'JFK', "note": "My usual layover when visiting family"}

        response = requests.post(url, data=payload)

        self.assertEqual(response.status_code, 401)

    @allure.feature('User save and delete favority airports')
    def test_allows_user_save_and_delete_their_favorite_airports(self):
        # Check that a user can create a favorite airport.
        url = f'{self.BASE_URL}/favorites'
        payload = {"airport_id": "JFK", "note": "My usual layover when visiting family"}

        response = requests.post(url, data=payload, auth=BearerAuth(self.AIRPORT_API_KEY))
        response_body = response.json()
        print('robert', response_body)
        attributes = response_body["data"]["attributes"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(attributes["airport"]["name"], 'John F Kennedy International Airport')
        self.assertEqual(attributes["note"], 'My usual layover when visiting family')

        favorite_id = response_body["data"]["id"]

        # Check that a user can update the note of the created favorite.
        payload = {"note": 'My usual layover when visiting family and friends'}
        url = f'{self.BASE_URL}/favorites/{favorite_id}'

        response = requests.put(url, data=payload, auth=BearerAuth(self.AIRPORT_API_KEY))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(attributes["note"], 'My usual layover when visiting family')

        # Check that a user can delete the created favorite.
        response = requests.delete(url, data=payload, auth=BearerAuth(self.AIRPORT_API_KEY))
        self.assertEqual(response.status_code, 204)

        # Verify that the record was deleted.
        response = requests.get(url, data=payload, auth=BearerAuth(self.AIRPORT_API_KEY))
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
