"""
TODO: Docstring
"""
from enum import Enum
import numpy as np
from setuptools._distutils.util import strtobool
from backend.packages import Package, PackageSize


MAX_NUM_OF_PACKAGES: int = 8
MAX_NUM_OF_LARGE_PACKAGES: int = 2
MAX_NUM_OF_SMALL_PACKAGES: int = 6


class Movement(Enum):
    """
    TODO: Docstring
    """
    NONE = 0
    LEFT = 1
    RIGHT = 2


class Location(Enum):
    """
    TODO: Docstring
    """
    OUTSIDE = 0
    IN_ELEVATOR = 1
    INSIDE_TRAM = 2


class StatusLED(Enum):
    """
    TODO: Docstring
    """
    ERROR = -1
    BOOTING = 0
    READY = 1
    WAITING = 2
    ALARM = 3
    HUMAN_INTERACTION = 4
    WORK_COMPLETED = 5
    REVERSING = 6
    PARKING = 7
    ERROR_INTERACTION = 8
    EMERGENCY = 9
    HELP_REQUEST = 10


class Robot:
    """
    A robot that can carry packages, manage its battery status, control lights, 
    and perform various actions such as parking and opening doors.
    The attributes of this robot are private, but can be interacted with setter/getter methods.
    """
    _status: dict[bool] = {"is_charging": False,
                           "is_door_opened": False, "is_parked": False, "is_reversing": False}
    _battery_status: float
    _led_rgb: tuple[int, int, int]
    _packages: list[Package] = []
    _current_destination: str = None
    _current_position: str = "Karlsruhe, Hauptbahnhof, Germany"

    def __init__(self, is_parked=False, is_door_opened=False,
                 is_reversing: bool = False,
                 is_charging: bool = False, battery_status: float = 100.0,
                 led_rgb: tuple[int, int, int] = (0, 0, 0), current_position: str = "Karlsruhe, Hauptbahnhof, Germany"):
        self.status["is_charging"] = is_charging
        self.status["is_door_opened"] = is_door_opened
        self.status["is_parked"] = is_parked
        self.status["is_reversing"] = is_reversing
        self.battery_status = battery_status
        self.led_rgb = led_rgb
        self.current_position = current_position

    def __str__(self) -> str:
        # TODO: Good overview string of Robot instance
        return f"Robot | Amount of Packages: {len(self._packages)} | Status: {
            self.status} | Packages: {self._packages}"

    ########################################################################################
    # Setters/Getters                                                                      #
    ########################################################################################
    @property
    def status(self) -> dict[bool]:
        """
        Lookup the boolean values of the robot.
        """
        return self._status

    @status.setter
    def status(self, **kwargs):
        """
        Setter for the boolean values.
        Accepts is_charging; is_door_opened; is_parked; is_reversing.
        """
        for key, value in kwargs.items():
            if key in ("is_charging", "is_door_opened", "is_parked", "is_reversing"):
                try:
                    setattr(self, f"_{key}", strtobool(value) if hasattr(
                        strtobool, "__call__") else bool(value))
                except (KeyError, ValueError):
                    continue

    @property
    def battery_status(self) -> float:
        """
        Battery status (float); 0.0 < x 100.0.
        """
        return self._battery_status

    @battery_status.setter
    def battery_status(self, val: float):
        """
        Cleans any given query string and returns a valid battery status (between 0.0 - 100.0 %).
        """
        try:
            val = float(val)
            self._battery_status = max(0.0, min(val, 100.0))
        except (TypeError, ValueError):
            self._battery_status = 100.0

    @property
    def led_rgb(self) -> list[int, int, int]:
        """
        TODO DOCSTRING
        """
        return self._led_rgb

    @led_rgb.setter
    def led_rgb(self, led: list[int, int, int] = None):
        """
        This sets the light of the LED. A LED is in RGB; it is an 8bit unisgned integer.
        """
        self._led_rgb = [0, 0, 0]
        if led is None or len(led) != 3:
            return

        try:
            if len(led) != 3:
                self._led_rgb = [0, 0, 0]
                return
            r, g, b = np.clip(led, 0, 255)
            self._led_rgb = [r, g, b]
        except Exception as e:
            print(e)
            self._led_rgb = [0, 0, 0]
            return

    def get_robot_status(self):
        """
        Returns the entire current status of any given robot.
        """
        params = {
            "status": self.status,
            "battery_status": self.battery_status,
            "led_rgb": self.led_rgb,
            "packages": self.packages,
            "current_position": self.current_position,
            "current_destination": self.current_destination
        }
        return params

    ########################################################################################
    # Positional                                                                           #
    ########################################################################################
    @property
    def current_destination(self) -> str | None:
        return self._current_destination

    @current_destination.setter
    def current_destination(self, val: str):
        self._current_destination = val

    @property
    def current_position(self) -> str:
        return self._current_position

    @current_position.setter
    def current_position(self, val: str):
        self._current_position = val
        if val is None:
            self._current_position = "Karlsruhe Hauptbahnhof, Karlsruhe, Germany"

    ########################################################################################
    # Packages                                                                             #
    ########################################################################################

    @property
    def packages(self) -> list[Package]:
        if self._packages is None:
            self.packages = []
        return self._packages

    @packages.setter
    def packages(self, val: list[Robot]):
        self._packages = val

    def add_package(self, pkg: Package) -> int:
        """Adds a package to a robot. Returns -1 in case of an error; 0 otherwise."""
        if self._packages is None:
            self._packages = []
        if len(self._packages) >= MAX_NUM_OF_PACKAGES:
            return -1
        amount_small_packages: int = sum(
            1 for package in self.packages if package.size == PackageSize.SMALL)
        amount_large_packages: int = sum(
            1 for package in self.packages if package.size == PackageSize.LARGE)
        if pkg.size is PackageSize.SMALL and amount_small_packages >= MAX_NUM_OF_SMALL_PACKAGES:
            return -1
        if pkg.size is PackageSize.LARGE and amount_large_packages >= MAX_NUM_OF_SMALL_PACKAGES:
            return -1

        # TODO: Add Dijkstra in case multiple destinations exist within more packages.
        # TODO: Right now, it only adds a singular destination, but never changes.
        if self._current_destination is None:
            self._current_destination = pkg.destination
        self._packages.append(pkg)
        return 0
