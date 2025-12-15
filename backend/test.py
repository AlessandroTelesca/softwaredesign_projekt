
import unittest
from unittest import result
from urllib import response
import requests
from robot import Movement
from robot import Location
from robot import StatusLED
from robot import Robot
from app import json_response




class TestAPIModule(unittest.TestCase):
    
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
        url = "http://localhost:5000/api/robot/create?battery_status=40"   
        response = requests.get(url)
        print(response.json())



if __name__ == '__main__':
    unittest.main() 
                




