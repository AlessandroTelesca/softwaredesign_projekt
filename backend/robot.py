"""
TODO: Docstring
"""
from enum import Enum


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
    TODO: Docstring
    """
    is_parked: bool
    is_door_opened: bool
    is_reversing: bool
    is_charging: bool

    battery_status: float = 100.0
    message: str
    led_rgb: tuple[int, int, int]

    def __init__(self):
        """
        TODO: Docstring
        """
