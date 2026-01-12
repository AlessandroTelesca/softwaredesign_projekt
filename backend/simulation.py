"""
Singleton for the Flask backend.
Provides a global Simulation instance.
"""
from datetime import date, time, datetime
from backend.robot import Robot


class Simulation:
    """
    A simulation environment that holds multiple robots and manages the simulation time.

    robots (list[Robot]): A list of robots in the simulation.
    current_date (date): The current date in the simulation.
    current_time (time): The current time in the simulation.
    time_per_tick (int): The amount of simulated time that passes per tick, in seconds.
    """
    #robots: list[Robot] = []
    time_per_tick: int = 1
    _cur_date: date
    _cur_time: time
    _robots: list[Robot] = []

    def __init__(self, robots: list[Robot] = [], current_date: date = date.today(), current_time: time = time(), time_per_tick: int = 1):
        self.current_date = current_date
        self.current_time = current_time
        self.robots = robots
        self.time_per_tick = time_per_tick

    def __str__(self) -> str:
        string = f"Date: {self.current_date} | Time: {self.current_time} | Time Per Tick: {
            self.time_per_tick} | Amount of Robots: {len(self.robots)}"
        return string

    ########################################################################################
    # Setters/Getters                                                                      #
    ########################################################################################
    @property
    def current_date(self) -> date:
        return self._cur_date

    @current_date.setter
    def current_date(self, day: int = -1, month: int = -1, year: int = -1):
        if day == -1 or month == -1 or year == -1:
            self._cur_date = date.today()
            return
        self._cur_date = date(year=year, month=month, day=day)

    @property
    def current_time(self) -> time:
        return self._cur_time

    @current_time.setter
    def current_time(self, cur_time: time):
        if cur_time is None:
            self._cur_time = time()
            return
        self._cur_time = cur_time

    @property
    def robots(self) -> list[Robot]:
        return self._robots
    
    @robots.setter
    def robots(self, robot: Robot = None):
        if robot:
            rbt: list[Robot] = self.robots
            rbt.append(robot)
            self._robots = rbt
    
    def reset(self):
        self._robots = []
