
import re
from tkinter import N
import unittest
from unittest import result
from urllib import response
import requests
from robot import Movement
from robot import Location
from robot import StatusLED
from robot import Robot
from app import json_response




class TestBatteryStatus(unittest.TestCase):
    
    def test_json_response(self):
            result = json_response({"key": "value"})
            self.assertEqual(result, '{"key": "value"}', "json_response did not return the expected JSON string.")

    def test_json_request_false(self):
        result = json_response({"hand": "error"})
        self.assertEqual (result, {"error": "error"}, "json_response did not return the expected")   

    def test_multiple_robot_create(self):
        for i in range(5):
            url = "http://localhost:5000/api/robot/create"
            response = requests.get(url)
            print(f"Request {i+1} returned: {response.json()}")
    
    def test_missing_battery_status(self):
            url = "http://localhost:5000/api/robot/create"
            response = requests.get(url)
            battery_status = response.json( )["status"]["battery_status"]
            print(f"Request with no battery_status parameter returned battery_status: {battery_status}")
    
    def test_change_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status=100"
        response = requests.get(url)
        battery_status = response.json()["status"]["battery_status"]
        print(f"Request with battery_status='100' returned battery_status: {battery_status}")

    def test_negative_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status=-10"
        response = requests.get(url)
        battery_status = response.json( )["status"]["battery_status"]
        print(f"Request with battery_status='-10' returned battery_status: {battery_status}")

    def test_string_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status=full"
        response = requests.get(url)
        battery_status = response.json()["status"]["battery_status"]
        print(f"Request with battery_status='full' returned battery_status: {battery_status}")

    def test_float_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status=75.5"
        response = requests.get(url)
        battery_status = response.json( )["status"]["battery_status"]
        print(f"Request with battery_status='75.5' returned battery_status: {battery_status}")

    def test_overflow_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status=150"
        response = requests.get(url)
        battery_status = response.json( )["status"]["battery_status"]
        print(f"Request with battery_status='150' returned battery_status: {battery_status}")

    def test_zero_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status=0"
        response = requests.get(url)
        battery_status = response.json( )["status"]["battery_status"]
        print(f"Request with battery_status='0' returned battery_status: {battery_status}")

    def test_empty_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status="
        response = requests.get(url)
        battery_status = response.json( )["status"]["battery_status"]
        if battery_status is None or battery_status== "":
            print("Request with battery_status='' returned battery_status: None")
        else:   
            print(f"Request with battery_status='' returned battery_status: {battery_status}")

    def test_number_and_string_battery_status(self):
        url = "http://localhost:5000/api/robot/create?battery_status=abc123"
        response = requests.get(url)
        battery_status = response.json( )["status"]["battery_status"]
        print(f"Request with battery_status='abc123' returned battery_status: {battery_status}")

    def test_special_char_battery_status(self):
        special_chars = ['@', '#', '$', '%', '&', '*', '!', '^', '()', '+-']
        for char in special_chars:
            url = f"http://localhost:5000/api/robot/create?battery_status={char}"
            response = requests.get(url)
            battery_status = response.json()["status"]["battery_status"]
            print(f"Request with battery_status='{char}' returned battery_status: {battery_status}")


if __name__ == '__main__':
    unittest.main() 
                




