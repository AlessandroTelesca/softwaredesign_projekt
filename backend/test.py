"""
Unit tests for the API middleware.

This module tests the API endpoints and functionalities, including:
- GET and POST request handling
- Robot creation and validation
- Battery status validation
"""
import unittest
from joblib import PrintTime
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


# class TestAPIModule(unittest.TestCase):
#     """
#     Right now, it tests a basic call of the Hello World function of the middleware.
#     Robot testing: Creation without parameters; creation with strings in battery status.
#     TODO: Add more tests.
#     """

#     def test_get_request(self):
#         """
#         This tests if a get request is possible by calling the Hello, World function from the middleware.
#         """
#         response = get_request("/hello")
#         self.assertIsInstance(response, requests.Response)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"message": "Hello World"})
        
#         print("GET request successful.")
    
#     def test_robot_create(self, test_count: int = 1):
#         """
#         Tests if it is possible to create a robot with an empty query string.
#         test_count: Amount of robots created; defaults to 1.
#         """
#         for _ in range(test_count):
#             response = post_request("/robot/create")
#             self.assertEqual(response.status_code, 200)
#             self.assertIsInstance(response.json(), dict)

#         print("create robot tested.")
    
#     def test_valid_battery_status(self):
#         """
#         Checks if the query parameters for the battery status are valid (e.g. is float or int; not <0.0, not >100.0).
#         """
#         test_cases: list = ["abc", 53, 3.14, -3.0, 101.0]

#         for test_value in test_cases:
#             # Send POST request.
#             str_response = post_request(
#                 "/robot/create", params={"battery_status": test_value}
#             )
#             battery_status = str_response.json()[
#                 "status"]["battery_status"]

#             # Check if POST request was acknowledged.
#             self.assertEqual(str_response.status_code, 200)
#             self.assertIsInstance(battery_status, float)

#             # Checks if given test case was valid input to begin with.
#             is_valid_input: bool = (
#                 isinstance(test_value, (int, float))
#                 and 0.0 <= test_value <= 100.0
#             )
#             if is_valid_input:
#                 self.assertEqual(
#                     battery_status, test_value, f"Expected: {
#                         test_value} | Result: {battery_status}")

#             self.assertTrue(0.0 <= battery_status <= 100.0)

#         print("Battery status tested.")

#     def test_valid_led_status(self):
        
#         """Test possible LED status by sending POST requests to /robot/create endpoint.
#         """

        
#         test_cases: list = [[0, 0, 0], [255, 255, 255]]
#         # Send POST requests with different LED status
#         for test_value in test_cases:
#             response = post_request(
#                 "/robot/create", params={"led_rgb": test_value}
#             )
#             # Check response code
#             self.assertEqual(response.status_code, 200)
#             # look if response is empty
#             self.assertTrue(
#                 response.text.strip(),
#                 f"Empty response body for input {test_value}",
#             )

#             try:
#                 str_response = response.json()
#             except ValueError:
#                 self.fail(f"Response is not valid JSON: {response.text}")
            
#             self.assertIn("status", str_response)
#             self.assertIn("led_rgb", str_response["status"])
#             # Check if status is list of3 ints
#             led_status = str_response["status"]["led_rgb"]
#             self.assertIsInstance(led_status, list)
#             self.assertEqual(len(led_status), 3)

#         print("LED status tested.")
    
#     def test_charging_status(self):
#             test_cases: list=[True, False, 'true', 'sergsrg', 23, 4.5, 'a']
#             for i in test_cases: 
#                 charge_post= post_request(
#                     "/robot/create", params={"is_charging": i}
#                 )
               
#                 is_charging=charge_post.json()["status"]["status"]["is_charging"]
#                 self.assertIsInstance(is_charging, bool)

#             print("Charging status tested.")
    
#     def test_parking(self):
#             test_cases: list=[True, False, 'true,' 'jawohlja', 34, 5.4, 'a']
#             for i in test_cases:
#                 park_post= post_request(
#                     "/robot/create", params={"is_parked": i}
#                 )
#                 is_parking=park_post.json()["status"]["status"]["is_parked"]
#                 self.assertIsInstance(is_parking, bool)

#             print("Parking status tested.")
   
#     def test_robot_status_flags(self):
#         """tests robot status flags 
#         """
        
#         test_cases = [True, False, "true", "sergsrg", 23, 4.5, "a"]

#         status_flags = [
#             "is_charging",
#             "is_parked",
#             "is_reversing",
#             "is_door_opened"
#         ]

#         for flag in status_flags:
#             for value in test_cases:
#                 response = post_request(
#                     "/robot/create",
#                     params={flag: value}
#                 )

#                 status_value = response.json()["status"]["status"][flag]
#                 self.assertIsInstance(status_value, bool)

#         print("Robot status flags tested.")
    
#     def test_delete_robot_by_id(self):
#         """Test if a robot is deletable by his ID via /robot/delete/<robot_id> endpoint.
#         """
        
#         robot_id = 0
#         # Create two robots
#         post_request("/robot/create")
#         post_request("/robot/create")

#         # Delete robot 0
#         response = post_request(f"/robot/delete/{robot_id}")
#         str_response = response.json()

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(str_response["message"], f"Robot {robot_id} deleted successfully.")
#         self.assertIn("robot_count", str_response)

#         # Verify robot deletion
#         read_response = get_request(f"/robot/read/{robot_id}")
#         self.assertEqual(read_response.status_code, 404)
        
#         print("Delete robot by ID tested.")

    

# class TestAPIModuleSim(unittest.TestCase):   

#     def test_sim_reset(self):
#                 """""
#                 Test if the Simulation resets properly by sending a POST request to /sim/reset endpoint.
#                 """""
#                 #create a robot
#                 post_request("/robot/create") 
                
#                 #send POST request to reset simulation
#                 response = post_request("/sim/reset")
#                 #check response status code and message
#                 self.assertEqual(response.status_code, 200)
#                 self.assertEqual(response.text.strip(), '{"message":"Simulation reset successfully."}')
                
#                 print("Simulation reset tested.")

#     def test_setting_time(self):
#         """
#         Testing Time testcases by sending POST requests to /sim/set_time endpoint.
#         """
#         test_cases: list = [
#             ({"hours": "10", "minutes": "30", "seconds": "45"}, 200),
#             ({"hours": "25", "minutes": "30"}, 400),  
#             ({"hours": "10", "minutes": "61"}, 400),  
#         ]
#         # POST requests with time settings
#         for params, expected_status in test_cases:
#             response = post_request("/sim/set_time", params=params)
#             # Check response status code
#             self.assertEqual(response.status_code, expected_status)
        
#         print("Simulation time setting tested.")


#     def test_heartbeat(self):
#         """
#         Tests heartbeat by checking if the response contains expected keys and types.
#         """
#         # Send GET request to /sim/heartbeat
#         response = get_request("/sim/heartbeat")
#         self.assertEqual(response.status_code, 200)

#         data = response.json()
#         # Check for expected keys and their types
#         expected = {
#             "ticks": int,
#             "date": str,
#             "time": str,
#         }
#         # assert key and its type
#         for key, expected_type in expected.items():
#             self.assertIn(key, data)
#             self.assertIsInstance(data[key], expected_type)
        
#         print("Simulation heartbeat tested.")

class TestAPIModuleMap(unittest.TestCase):
    def test_map_GET(self):
        """
        Tests GET request for map endpoint by checking if the response contains a map.
        """
        # Send GET request
        response = get_request("/map")
        # Check response status code and presence of map
        self.assertEqual(response.status_code, 200)
        self.assertIn("map", response.json())
        
        print("Map GET request tested.")

    def test_map_route_POST_success(self): ##### ACHTUNG AI ######
        """Tests map route
        """
        # Send POST request
        response = requests.post(
            "http://localhost:5000/api/map/route",
            data={"start": "Karlsruhe Hauptbahnhof, Germany", "end": "Karlsruhe Durlach Bahnhof, Germany"},
            timeout=60  # Timeout to 60 sec because map generation might take some time
        )

        self.assertEqual(response.status_code, 200)
        # Check if response contains expected keys
        data = response.json()
        for key in ("map", "start", "end", "route_color"):
            self.assertIn(key, data)
        # Check values
        self.assertEqual(data["start"], "Karlsruhe Hauptbahnhof, Germany")
        self.assertEqual(data["end"], "Karlsruhe Durlach Bahnhof, Germany")
        # Default route color is red (#d32f2f)
        self.assertEqual(data["route_color"], "#d32f2f")
        # Check if map is a non-empty string
        self.assertIsInstance(data["map"], str)
        self.assertTrue(data["map"])

        print("Map route POST request (success) tested.")

    def test_map_lines(self):
        """
        Tests map/lines endpoint by checking if the response contains a list of lines.
        """
        # Send GET request
        response = get_request("/map/lines")
        # Check response status code
        self.assertEqual(response.status_code, 200)
        # Check if response contains 'lines' key with a list
        data = response.json()
        self.assertIn("lines", data)
        self.assertIsInstance(data["lines"], list)
        # assert the list is not empty
        self.assertTrue(len(data["lines"]) > 0)

        print("Map lines tested")

if __name__ == "__main__":
    unittest.main()
