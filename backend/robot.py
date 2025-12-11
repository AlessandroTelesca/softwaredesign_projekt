"""
TODO: Docstring
"""
from enum import Enum
from packages import Package


class Movement(Enum):
    """
    TODO: Docstring
    """
    NONE = 0,
    LEFT = 1,
    RIGHT = 2


class Location(Enum):
    """
    TODO: Docstring
    """
    OUTSIDE = 0,
    IN_ELEVATOR = 1,
    INSIDE_TRAM = 2


class StatusLED(Enum):
    """
    TODO: Docstring
    """
    ERROR = -1,
    BOOTING = 0,
    READY = 1,
    WAITING = 2,
    ALARM = 3,
    HUMAN_INTERACTION = 4,
    WORK_COMPLETED = 5,
    REVERSING = 6,
    PARKING = 7,
    ERROR_INTERACTION = 8,
    EMERGENCY = 9,
    HELP_REQUEST = 10


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

    def __init__(self, is_parked, is_door_opened,
                 is_reversing: bool,
                 is_charging: bool, battery_status: float,
                 message: str, led_rgb: tuple[int, int, int],
                 packages: list[Package]):
        self.is_parked = is_parked
        self.is_door_opened = is_door_opened
        self.is_reversing = is_reversing
        self.is_charging = is_charging
        self.battery_status = battery_status
        self.message = message
        self.led_rgb = led_rgb
        self.packages = packages
