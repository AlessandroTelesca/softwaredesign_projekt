"""
Singleton for the Flask backend.
Provides a global Simulation instance.
"""
from robot import Robot
from datetime import date, time

class Simulation:
    """
    A simulation environment that holds multiple robots and manages the simulation time.

    robots (list[Robot]): A list of robots in the simulation.
    current_date (date): The current date in the simulation.
    current_time (time): The current time in the simulation.
    time_per_tick (int): The amount of simulated time that passes per tick, in seconds.
    """
    robots: list[Robot] = []
    current_date: date
    current_time: time
    time_per_tick: int = 1

    def __init__(self, robots: list[Robot] = [], current_date: date = date.today(), current_time: time = time(), time_per_tick: int = 1):
        self.current_date = current_date
        self.current_time = current_time
        self.robots = robots
        self.time_per_tick = time_per_tick