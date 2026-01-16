"""
Singleton for the Flask backend.
Provides a global Simulation instance.
"""
import threading
from backend.robot import Robot
from time import sleep
import datetime as dt


class Simulation:
    """
    A simulation environment that holds multiple robots and manages the simulation time.

    robots (list[Robot]): A list of robots in the simulation.
    time_per_tick (int): The amount of simulated time that passes per tick, in seconds.
    seconds_per_tick (int): The amount of seconds that pass with each tick.
    date_and_time (datetime): The current date and time.
    """
    _seconds_per_tick: int = 1
    time_per_tick: int = 60
    _date_and_time: dt = None
    _robots: list[Robot] = []
    _ticks: int = 0
    thread: threading.Thread = None

    def __init__(self, robots: list[Robot] = [], time_per_tick: int = 1):
        self.robots = robots
        self.seconds_per_tick = time_per_tick

        self.thread = threading.Thread(target=self.timer_ticks)
        self.thread.daemon = True
        self.thread.start()

    def __str__(self) -> str:
        string = f"Datetime: {self.date_and_time.strftime("%d/%m/%Y, %H:%M")} | Ticks: {self.ticks} | Seconds Per Tick: {
            self.seconds_per_tick} | Simulated Time Per Tick: {self.time_per_tick}s | Amount of Robots: {len(self.robots)}"
        return string

    ########################################################################################
    # Setters/Getters                                                                      #
    ########################################################################################
    @property
    def date(self) -> str:
        """Returns the current date as a string."""
        return self.date_and_time.strftime("%d.%m.%y")

    @property
    def time(self) -> str:
        """Returns the current time as a string."""
        return self.date_and_time.strftime("%H:%M")

    @property
    def date_and_time(self) -> dt.datetime:
        """
        If there is no given date, will create the current time stamp. 
        Otherwise simply returns its value.
        """
        if self._date_and_time is None:
            self._date_and_time = dt.datetime.now()
        return self._date_and_time

    @date_and_time.setter
    def date_and_time(self, date_and_time: dt.datetime):
        self._date_and_time = date_and_time

    @property
    def ticks(self) -> int:
        return self._ticks

    @property
    def robots(self) -> list[Robot]:
        return self._robots

    @robots.setter
    def robots(self, robot: Robot = None):
        if robot:
            rbt: list[Robot] = self.robots
            rbt.append(robot)
            self._robots = rbt

    @property
    def seconds_per_tick(self) -> int:
        return self._seconds_per_tick

    @seconds_per_tick.setter
    def seconds_per_tick(self, val: int):
        try:
            val = int(val)
            if val >= 1:
                self._seconds_per_tick = val
        except TypeError:
            return

    def reset(self):
        """This fully resets the simulation. Sets a new start date at current time."""
        self._robots = []
        self._ticks = 0
        self._date_and_time = dt.datetime.now()

    def timer_ticks(self):
        """
        Runs off an autonomous thread.
        Ensures simulation is running asynchronously with the backend.
        Waits for an alotted time with self.seconds_per_tick.
        """
        while True:
            sleep(self.seconds_per_tick)
            self._ticks += 1
            new_time = self.date_and_time + \
                dt.timedelta(0, seconds=self.time_per_tick)
            self._date_and_time = new_time
