"""
TODO
"""
from enum import Enum

STD_START: str = "Karlsruhe Hauptbahnhof, Germany"
STD_DESTINATION: str = "Karlsruhe Durlach Bahnhof, Germany"


class PackageSize(Enum):
    """
    TODO: Docstring
    """
    SMALL = 0
    LARGE = 1


class Package:
    """
    TODO: Docstring
    """
    _start: str = "Karlsruhe Hauptbahnhof"
    _destination: str
    _size: PackageSize

    def __init__(self, start: str, destination:  str, size: str):
        """
        TODO: Docstring
        """
        self._start = start
        self._destination = destination
        self._size = size

    def __str__(self) -> str:
        return f"Package, Size {self._size.name}"

    @property
    def start(self) -> str:
        if self._start is None:
            self.start = "Karlsruhe Hauptbahnhof"
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def size(self) -> PackageSize:
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
