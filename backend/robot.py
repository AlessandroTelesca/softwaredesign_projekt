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
    # _is_charging: bool
    # _is_door_opened: bool
    # _is_parked: bool
    # _is_reversing: bool
    _status: dict[bool] = {"is_charging": False,
                           "is_door_opened": False, "is_parked": False, "is_reversing": False}

    _battery_status: float
    _message: str
    _led_rgb: tuple[int, int, int]
    _packages: list[Package] = []

    def __init__(self, is_parked, is_door_opened,
                 is_reversing: bool,
                 is_charging: bool, battery_status: float,
                 message: str, led_rgb: tuple[int, int, int],
                 packages: list[Package]):
        self._is_parked = is_parked
        self._is_door_opened = is_door_opened
        self._is_reversing = is_reversing
        self._is_charging = is_charging
        self.set_battery_status(battery=battery_status)
        self._message = message
        self._led_rgb = led_rgb
        self._packages = packages

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

    # @property
    # def is_charging(self) -> bool:
    #     return self._is_charging

    # @is_charging.setter
    # def is_charging(self, value):
    #     try:
    #         is_charging = strtobool(value)
    #         self._is_charging = is_charging
    #     except AttributeError:
    #         self._is_charging = bool(value)
    #     except ValueError:
    #         self._is_charging = False

    # @property
    # def is_door_opened(self) -> bool:
    #     return self._is_door_opened

    # @is_door_opened.setter
    # def is_door_opened(self, value):
    #     try:
    #         is_door_opened = strtobool(value)
    #         self._is_door_opened = is_door_opened
    #     except AttributeError:
    #         self._is_door_opened = bool(value)
    #     except ValueError:
    #         self._is_door_opened = False

    # @property
    # def is_parked(self) -> bool:
    #     return self._is_parked

    # @is_parked.setter
    # def is_parked(self, value):
    #     try:
    #         is_parked = strtobool(value)
    #         self._is_parked = is_parked
    #     except AttributeError:
    #         self._is_parked = bool(value)
    #     except ValueError:
    #         self._is_parked = False

    # @property
    # def is_reversing(self) -> bool:
    #     return self._is_reversing

    # @is_reversing.setter
    # def is_reversing(self, value):
    #     try:
    #         is_reversing = strtobool(value)
    #         self._is_reversing = is_reversing
    #     except AttributeError:
    #         self._is_reversing = bool(value)
    #     except ValueError:
    #         self._is_reversing = False

    def get_robot_status(self):
        """
        Returns the entire current status of any given robot.
        """
        params = {
            "status": self.status,
            # "is_parked": self._is_parked,
            # "is_door_opened": self._is_door_opened,
            # "is_reversing": self._is_reversing,
            # "is_charging": self._is_charging,
            "battery_status": self._battery_status,
            "message": self._message,
            "led_rgb": self._led_rgb,
            "packages": self._packages,
        }
        return params

    def set_battery_status(self, battery: float):
        """
        Cleans any given query string and returns a valid battery status (between 0.0 - 100.0 %).
        """
        # TODO: Rewrite this in accord with the other setter/getter methods.
        try:
            battery = float(battery)
            self._battery_status = max(0.0, min(battery, 100.0))
        except (TypeError, ValueError):
            self._battery_status = 100.0

    ########################################################################################
    # Packages                                                                             #
    ########################################################################################
    def add_new_package(self, size: PackageSize, start: str, destination: str):
        """
        TODO: Docstring
        """
        if len(self._packages) >= MAX_NUM_OF_PACKAGES:
            return
        amount_small_packages: int = sum(
            1 for package in self._packages if package.size == PackageSize.SMALL)
        amount_large_packages: int = sum(
            1 for package in self._packages if package.size == PackageSize.LARGE)

        if size is PackageSize.SMALL and amount_small_packages >= MAX_NUM_OF_SMALL_PACKAGES:
            return
        if size is PackageSize.LARGE and amount_large_packages >= MAX_NUM_OF_SMALL_PACKAGES:
            return
        pkg = Package(start=start, destination=destination, size=size)
        self._packages.append(pkg)
