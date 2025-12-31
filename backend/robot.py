"""
TODO: Docstring
"""
from enum import Enum
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
    _message: str
    _led_rgb: tuple[int, int, int]
    _packages: list[Package] = []

    def __init__(self, is_parked=False, is_door_opened=False,
                 is_reversing: bool = False,
                 is_charging: bool = False, battery_status: float = 100.0,
                 message: str = "", led_rgb: tuple[int, int, int] = (0, 0, 0)):
        self.status["is_charging"] = is_charging
        self.status["is_door_opened"] = is_door_opened
        self.status["is_parked"] = is_parked
        self.status["is_reversing"] = is_reversing
        self.battery_status = battery_status
        self.message = message
        self.led_rgb = led_rgb

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
        TODO: Docstring
        """
        return self._status

    @status.setter
    def status(self, **kwargs):
        """
        TODO: Docstring
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
        TODO: Docstring.
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
    def message(self) -> str:
        """
        TODO: Docstring.
        """
        return self._message

    @message.setter
    def message(self, val: str):
        """
        TODO Docstring
        """
        # TODO
        self._message = val

    @property
    def led_rgb(self) -> tuple[int, int, int]:
        """
        TODO DOCSTRING
        """
        return self._led_rgb

    @led_rgb.setter
    def led_rgb(self, led: tuple[int, int, int] = None):
        """
        TODO DOCSTRING
        """
        # TODO
        self._led_rgb = led

    def get_robot_status(self):
        """
        Returns the entire current status of any given robot.
        """
        params = {
            "status": self.status,
            "battery_status": self.battery_status,
            "message": self.message,
            "led_rgb": self.led_rgb,
            "packages": self.packages,
        }
        return params

    ########################################################################################
    # Packages                                                                             #
    ########################################################################################
    @property
    def packages(self) -> list[Package]:
        return self._packages

    @packages.setter
    def packages(self, size: PackageSize, start: str, destination: str):
        """
        TODO: Docstring
        """
        # TODO
        if self._packages is None:
            self._packages = []

        if len(self._packages) >= MAX_NUM_OF_PACKAGES:
            return False
        amount_small_packages: int = sum(
            1 for package in self.packages if package.size == PackageSize.SMALL)
        amount_large_packages: int = sum(
            1 for package in self.packages if package.size == PackageSize.LARGE)

        if size is PackageSize.SMALL and amount_small_packages >= MAX_NUM_OF_SMALL_PACKAGES:
            return False
        if size is PackageSize.LARGE and amount_large_packages >= MAX_NUM_OF_SMALL_PACKAGES:
            return False
        pkg = Package(start=start, destination=destination, size=size)
        self._packages.append(pkg)
        return True
    
    #def add_package():

