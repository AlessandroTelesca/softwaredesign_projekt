"""
Robot module.

Robot is the backend model for a simulated vehicle ("train").
It stores current state, packages, and (important for map simulation):
- progress: float in [0..1]
- position: (lat, lon) or None
- messages: event log (for /api/robot/read polling)

This file is intentionally simple and "student readable".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import threading
import time

from backend.packages import Package, PackageSize


MAX_NUM_OF_PACKAGES: int = 8
MAX_NUM_OF_LARGE_PACKAGES: int = 2
MAX_NUM_OF_SMALL_PACKAGES: int = 6


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


@dataclass
class Robot:
    """
    Robot model for the simulation.

    Fields used by the map simulation:
        progress: 0..1 overall progress along the route
        position: current (lat, lon)
        messages: list of event dicts
    """

    robot_id: int

    is_parked: bool = True
    is_door_opened: bool = False
    is_reversing: bool = False
    is_charging: bool = False

    battery_status: float = 100.0
    message: str = ""
    led_rgb: Tuple[int, int, int] = (0, 255, 0)

    # Simulation state for route driving
    progress: float = 0.0
    position: Optional[Tuple[float, float]] = None  # (lat, lon)

    _packages: List[Package] = field(default_factory=list, repr=False)

    # Message log for polling (thread-safe)
    _messages: List[Dict[str, Any]] = field(default_factory=list, repr=False)
    _last_message_id: int = field(default=0, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    # -------------------------
    # Packages
    # -------------------------
    @property
    def packages(self) -> List[Package]:
        return list(self._packages)

    @packages.setter
    def packages(self, val: List[Package]) -> None:
        if not isinstance(val, list) or not all(isinstance(p, Package) for p in val):
            raise TypeError("packages must be a list[Package].")
        self._validate_package_constraints(val)
        self._packages = list(val)

    def count_large_packages(self) -> int:
        return sum(1 for p in self._packages if getattr(p, "size", None) == PackageSize.LARGE)

    def count_small_packages(self) -> int:
        return sum(1 for p in self._packages if getattr(p, "size", None) == PackageSize.SMALL)

    @staticmethod
    def _validate_package_constraints(pkgs: List[Package]) -> None:
        if len(pkgs) > MAX_NUM_OF_PACKAGES:
            raise ValueError(f"Too many packages: max {MAX_NUM_OF_PACKAGES}.")

        large = sum(1 for p in pkgs if getattr(p, "size", None) == PackageSize.LARGE)
        small = sum(1 for p in pkgs if getattr(p, "size", None) == PackageSize.SMALL)

        if large > MAX_NUM_OF_LARGE_PACKAGES:
            raise ValueError(f"Too many large packages: max {MAX_NUM_OF_LARGE_PACKAGES}.")
        if small > MAX_NUM_OF_SMALL_PACKAGES:
            raise ValueError(f"Too many small packages: max {MAX_NUM_OF_SMALL_PACKAGES}.")

    # -------------------------
    # Simulation helpers
    # -------------------------
    def set_battery(self, value: float) -> None:
        self.battery_status = float(_clamp(float(value), 0.0, 100.0))

    def set_progress_position(self, progress: float, lat: float, lon: float) -> None:
        """Thread-safe update of progress/position."""
        with self._lock:
            # never go backwards (prevents "step back" bug)
            progress = float(_clamp(progress, 0.0, 1.0))
            if progress < self.progress:
                progress = self.progress
            self.progress = progress
            self.position = (float(lat), float(lon))

    def add_message(self, event: str, text: str, progress: float) -> int:
        """Append a message event and return its id."""
        with self._lock:
            self._last_message_id += 1
            msg = {
                "id": self._last_message_id,
                "robot_id": self.robot_id,
                "event": str(event),
                "text": str(text),
                "progress": float(_clamp(float(progress), 0.0, 1.0)),
                "ts": time.time(),
            }
            self._messages.append(msg)
            return self._last_message_id

    def get_messages_since(self, since_message_id: int) -> Tuple[int, List[Dict[str, Any]]]:
        """Return (last_message_id, messages with id > since_message_id)."""
        with self._lock:
            last_id = int(self._last_message_id)
            if since_message_id < 0:
                since_message_id = 0
            out = [m for m in self._messages if int(m.get("id", 0)) > since_message_id]
            return last_id, out

    # -------------------------
    # API serialization
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        # packages serialization (simple)
        pkg_list: List[Any] = []
        for p in self._packages:
            if hasattr(p, "to_dict") and callable(getattr(p, "to_dict")):
                pkg_list.append(p.to_dict())
            else:
                pkg_list.append(
                    {
                        "size": str(getattr(p, "size", "")),
                        "start": getattr(p, "start", None),
                        "destination": getattr(p, "destination", None),
                    }
                )

        with self._lock:
            pos = self.position
            prog = float(self.progress)

        return {
            "robot_id": self.robot_id,
            "is_parked": self.is_parked,
            "is_door_opened": self.is_door_opened,
            "is_reversing": self.is_reversing,
            "is_charging": self.is_charging,
            "battery_status": self.battery_status,
            "message": self.message,
            "led_rgb": self.led_rgb,
            "packages": pkg_list,
            "package_count": len(self._packages),
            "package_count_large": self.count_large_packages(),
            "package_count_small": self.count_small_packages(),
            "progress": prog,
            "position": pos,  # (lat, lon) or None
        }
