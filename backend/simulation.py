"""
Singleton for the Flask backend.
Provides a global Simulation instance.
"""
from robot import Robot

class Simulation:
    """
    TODO: Docstring
    """
    robots: list[Robot] = []

    def __init__(self, robots: list[Robot] = []):
        self.robots = robots
