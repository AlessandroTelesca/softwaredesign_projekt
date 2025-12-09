"""
TODO: Docstring
"""
from enum import Enum
from packages import Package, PackageSize


class Movement(Enum):
    """
    TODO: Docstring
    """
    LEFT = 0,
    RIGHT = 1


class Location(Enum):
    """
    TODO: Docstring
    """
    pass


class Lights(Enum):
    """
    TODO: Docstring
    """
    pass


class Robot:
    """
    A robot that can carry packages, manage its battery status, control lights, 
    and perform various actions such as parking and opening doors.
    """
    is_parked: bool
    is_door_opened: bool
    is_reversing: bool
    is_charging: bool

    battery_status: float = 100.0
    message: str
    led_rgb: tuple[int, int, int]
    packages: list[Package] = []

    def __init__(self, is_parked: bool = True, is_door_opened: bool = False,
                 is_reversing: bool = False,
                 is_charging: bool = False, battery_status: float = 100.0,
                 message: str = "", led_rgb: tuple[int, int, int] = (0, 0, 0),
                 packages: list[Package] = []):
        """
        TODO: Docstring
        """
        self.is_parked = is_parked
        self.is_door_opened = is_door_opened
        self.is_reversing = is_reversing
        self.is_charging = is_charging
        self.battery_status = battery_status
        self.message = message
        self.led_rgb = led_rgb
        self.packages = packages
