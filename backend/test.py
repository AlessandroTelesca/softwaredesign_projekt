"""
TODO: Docstring
"""
import unittest
import requests


class TestAPIModule(unittest.TestCase):
    """
    TODO: Docstring
    """
    # def test_json_response(self):
    #     result = json_response({"key": "value"})
    #     self.assertEqual(result, '{"key": "value"}', "json_response did not return the expected JSON string.")

    # def test_json_response_empty(self):
    #     result = json_response({"hand": "error"})
    #     self.assertEqual (result, {"error": "error"}, "json_response did not return the expected")

    # def test_GET_request(self):
    #     for i in range(10):
    #         url = "http://localhost:5000/api/robot/create"
    #         response = requests.get(url)
    #         print(response.json())

    def test_change_battery_status(self):
        """
        TODO: Docstring
        """
        url = "http://localhost:5000/api/robot/create?battery_status=40"
        response = requests.get(url)
        print(response.json())


if __name__ == '__main__':
    unittest.main()
