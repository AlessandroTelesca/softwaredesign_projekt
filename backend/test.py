"""
TODO: Docstring
"""
import json
import unittest
import requests
from app import json_response

URL: str = "http://localhost:5000/api"

def get_request(query: str, params = None) -> dict:
    """
    TODO: Docstring
    query: The GET request query; requires a / at the start.
    """
    return requests.get(URL + query, params)


def post_request(query: str, params = None):
    """
    TODO: Docstring
    """
    return requests.post(URL + query, params)


class TestAPIModule(unittest.TestCase):
    """
    TODO: Docstring
    """

    def test_json_response(self):
        result = json_response({"key": "value"})
        self.assertEqual(
            result, '{"key": "value"}', "json_response did not return the expected JSON string.")

    def test_get_request(self):
        """
        This tests if a get request is possible by calling the Hello, World function from the middleware.
        """
        response = get_request("/hello")
        self.assertEqual(response, {"message": "Hello World"})

    def test_robot_create(self, test_count: int = 1):
        """
        Tests if it is possible to create a robot with an empty query string.
        test_count: Amount of robots created; defaults to 1.
        """
        for _ in range(test_count):
            response = get_request("/robot/create")
            self.assertIsInstance(response, dict)
            print(response)

    def test_valid_battery_status(self):
        """
        Checks if the query parameters for the battery status are valid (e.g. is float; not <0.0, not >100.0)
        """
            #url = "http://localhost:5000/api/robot/create"
            #response = requests.get(url)
            #battery_status = response.json( )["status"]["battery_status"]
            #print(f"Request with no battery_status parameter returned battery_status: {battery_status}")
        response = get_request("/robot/create", params={"battery_status": "abc"})
        print(response)


    # def test_change_battery_status(self):
    #     """
    #     TODO: Docstring
    #     """
    #     input = "40"
    #     url = f"http://localhost:5000/api/robot/create?battery_status={input}"
    #     response = requests.get(url)
    #     battery_status = response.json()["status"]["battery_status"]
    #     battery_status_print(battery_status, input)

    # def test_negative_battery_status(self):
    #     url = "http://localhost:5000/api/robot/create?battery_status=-10"
    #     response = requests.get(url)
    #     battery_status = response.json( )["status"]["battery_status"]
    #     print(f"Request with battery_status='-10' returned battery_status: {battery_status}")

    # def test_string_battery_status(self):
    #     url = "http://localhost:5000/api/robot/create?battery_status=full"
    #     response = requests.get(url)
    #     battery_status = response.json()["status"]["battery_status"]
    #     print(f"Request with battery_status='full' returned battery_status: {battery_status}")

    # def test_float_battery_status(self):
    #     url = "http://localhost:5000/api/robot/create?battery_status=75.5"
    #     response = requests.get(url)
    #     battery_status = response.json( )["status"]["battery_status"]
    #     print(f"Request with battery_status='75.5' returned battery_status: {battery_status}")

    # def test_overflow_battery_status(self):
    #     url = "http://localhost:5000/api/robot/create?battery_status=150"
    #     response = requests.get(url)
    #     battery_status = response.json( )["status"]["battery_status"]
    #     print(f"Request with battery_status='150' returned battery_status: {battery_status}")

    # def test_zero_battery_status(self):
    #     url = "http://localhost:5000/api/robot/create?battery_status=0"
    #     response = requests.get(url)
    #     battery_status = response.json( )["status"]["battery_status"]
    #     print(f"Request with battery_status='0' returned battery_status: {battery_status}")

    # def test_empty_battery_status(self):
    #     url = "http://localhost:5000/api/robot/create?battery_status="
    #     response = requests.get(url)
    #     battery_status = response.json( )["status"]["battery_status"]
    #     if battery_status is None or battery_status== "":
    #         print("Request with battery_status='' returned battery_status: None")
    #     else:
    #         print(f"Request with battery_status='' returned battery_status: {battery_status}")

    # def test_number_and_string_battery_status(self):
    #     url = "http://localhost:5000/api/robot/create?battery_status=abc123"
    #     response = requests.get(url)
    #     battery_status = response.json( )["status"]["battery_status"]
    #     print(f"Request with battery_status='abc123' returned battery_status: {battery_status}")

    # def test_special_char_battery_status(self):
    #     special_chars = ['@', '#', '$', '%', '&', '*', '!', '^', '()', '+-']
    #     for char in special_chars:
    #         url = f"http://localhost:5000/api/robot/create?battery_status={char}"
    #         response = requests.get(url)
    #         battery_status = response.json()["status"]["battery_status"]
    #         print(f"Request with battery_status='{char}' returned battery_status: {battery_status}")


if __name__ == '__main__':
    unittest.main()
