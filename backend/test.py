"""
TODO: Docstring
"""
import unittest
import requests
from app import json_response

URL: str = "http://localhost:5000/api"


def get_request(query: str, params=None) -> dict:
    """
    Sends a GET request with the given parameters.
    query: The GET request query; requires a / at the start.
    """
    return requests.get(URL + query, params)


def post_request(query: str, params=None):
    """
    Sends a POST request with the given parameters.
    """
    return requests.post(URL + query, params)


class TestAPIModule(unittest.TestCase):
    """
    Right now, it tests a basic call of the Hello World function of the middleware.
    Robot testing: Creation without parameters; creation with strings in battery status.
    TODO: Add more tests.
    """

    def test_get_request(self):
        """
        This tests if a get request is possible by calling the Hello, World function from the middleware.
        """
        response = get_request("/hello")
        self.assertIsInstance(response, requests.Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_robot_create(self, test_count: int = 1):
        """
        Tests if it is possible to create a robot with an empty query string.
        test_count: Amount of robots created; defaults to 1.
        """
        for _ in range(test_count):
            response = post_request("/robot/create")
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json(), dict)

    def test_valid_battery_status(self):
        """
        Checks if the query parameters for the battery status are valid (e.g. is float; not <0.0, not >100.0)
        """
        validity_check = ["abc", 53, 3.14, -3.0, 101.0]

        for i in range(len(validity_check)):
            str_response = post_request(
                "/robot/create", params={"battery_status": validity_check[i]}
            )
            battery_status = str_response.json()[
                "status"]["battery_status"]
            self.assertEqual(str_response.status_code, 200)
            self.assertIsInstance(battery_status, float)
            self.assertTrue(battery_status >= 0.0 and battery_status <= 100.0)


if __name__ == "__main__":
    unittest.main()
