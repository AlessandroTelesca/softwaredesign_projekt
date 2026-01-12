"""
Unit tests for the API middleware.

This module tests the API endpoints and functionalities, including:
- GET and POST request handling
- Robot creation and validation
- Battery status validation
"""
import unittest
import requests
import test

from backend import robot

URL: str = "http://localhost:5000/api"
TIMEOUT: int = 5


def get_request(query: str, params=None) -> requests.Response:
    """
    Sends a GET request with the given parameters.
    query: The GET request query; requires a / at the start.
    """
    return requests.get(URL + query, params=params, timeout=TIMEOUT)


def post_request(query: str, params=None) -> requests.Response:
    """
    Sends a POST request with the given parameters.
    """
    return requests.post(URL + query, params=params, timeout=TIMEOUT)


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
        Checks if the query parameters for the battery status are valid (e.g. is float or int; not <0.0, not >100.0).
        """
        test_cases: list = ["abc", 53, 3.14, -3.0, 101.0]

        for test_value in test_cases:
            # Send POST request.
            str_response = post_request(
                "/robot/create", params={"battery_status": test_value}
            )
            battery_status = str_response.json()[
                "status"]["battery_status"]

            # Check if POST request was acknowledged.
            self.assertEqual(str_response.status_code, 200)
            self.assertIsInstance(battery_status, float)

            # Checks if given test case was valid input to begin with.
            is_valid_input: bool = (
                isinstance(test_value, (int, float))
                and 0.0 <= test_value <= 100.0
            )
            if is_valid_input:
                self.assertEqual(
                    battery_status, test_value, f"Expected: {
                        test_value} | Result: {battery_status}")

            self.assertTrue(0.0 <= battery_status <= 100.0)

   
    def test_valid_led_status(self):
        test_cases: list = [[0, 0, 0], [255, 255, 255]]

        for test_value in test_cases:
            response = post_request(
                "/robot/create", params={"led_rgb": test_value}
            )

            self.assertEqual(response.status_code, 200)

            self.assertTrue(
                response.text.strip(),
                f"Empty response body for input {test_value}",
            )

            try:
                data = response.json()
            except ValueError:
                self.fail(f"Response is not valid JSON: {response.text}")

            self.assertIn("status", data)
            self.assertIn("led_rgb", data["status"])

            led_status = data["status"]["led_rgb"]
            self.assertIsInstance(led_status, list)
            self.assertEqual(len(led_status), 3)


    def test_charging_status(self):
            test_cases: list=[True, False, 'true', 'sergsrg', 23, 4.5, 'a']
            for i in test_cases: 
                charge_post= post_request(
                    "/robot/create", params={"is_charging": i}

                )
                is_charging=charge_post.json()["status"]["status"]["is_charging"]
                self.assertIsInstance(is_charging, bool)
    def test_parking(self):
            test_cases: list=[True, False, 'true,' 'jawohlja', 34, 5.4, 'a']
            for i in test_cases:
                park_post= post_request(
                    "/robot/create", params={"is_parked": i}
                )
                is_parking=park_post.json()["status"]["status"]["is_parked"]
                self.assertIsInstance(is_parking, bool)
    def test_robot_status_flags(self):
        test_cases = [True, False, "true", "sergsrg", 23, 4.5, "a"]

        status_flags = [
            "is_charging",
            "is_parked",
            "is_reversing",
            "is_door_opened"
        ]

        for flag in status_flags:
            for value in test_cases:
                response = post_request(
                    "/robot/create",
                    params={flag: value}
                )

                status_value = response.json()["status"]["status"][flag]
                self.assertIsInstance(status_value, bool)


    def sim_reset(self):
        #create a robot
        post_request("/robot/create") 
        #send POST request to reset simulation
        response = post_request("/sim/reset")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip(), "")


    def test_delete_robot_by_id(self):
        robot_id = 0
        # create 2 robots
        post_request("/api/robot/create")
        post_request("/api/robot/create")

        # Delete robot with id 0
        response = post_request(f"/api/robot/delete/{robot_id}")
        self.assertEqual(response.status_code, 200, response.text)

        data = response.json()
        self.assertEqual(data["message"], f"Robot {robot_id} deleted successfully.")

        # Verify deletion
        read_response = get_request(f"/api/robot/read/{robot_id}")
        self.assertEqual(read_response.status_code, 404)






if __name__ == "__main__":
    unittest.main()
