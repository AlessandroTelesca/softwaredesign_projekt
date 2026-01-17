"""
Robot module.

This module defines the Robot class used by the backend simulation and API layer.
A robot represents an autonomous delivery unit that can carry packages and expose
its current state (doors, charging, reversing, LEDs, battery, etc.).

Responsibilities:
- Store and manage robot state
- Handle package assignment and validation
- Enforce package constraints:
  - max 8 packages total
  - max 2 large packages
  - max 6 small packages
- Provide serialization helpers for API responses

The Robot class is intended to be used by the Simulation singleton and exposed
through Flask endpoints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from backend.packages import Package, PackageSize


MAX_NUM_OF_PACKAGES: int = 8
MAX_NUM_OF_LARGE_PACKAGES: int = 2
MAX_NUM_OF_SMALL_PACKAGES: int = 6


def _is_bool(v: Any) -> bool:
    return isinstance(v, bool)


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float))


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


@dataclass
class Robot:
    """
    Robot model for the simulation.

    Attributes:
        robot_id: Unique ID of the robot (typically assigned by Simulation).
        is_parked: Whether the robot is currently parked.
        is_door_opened: Whether the robot's door is open.
        is_reversing: Whether the robot is reversing.
        is_charging: Whether the robot is currently charging.
        battery_status: Battery level in percent [0..100].
        message: Free status message (debug/info).
        led_rgb: LED color as (r, g, b) with values [0..255].
        packages: List of assigned packages.
    """

    robot_id: int

    is_parked: bool = True
    is_door_opened: bool = False
    is_reversing: bool = False
    is_charging: bool = False

    battery_status: float = 100.0
    message: str = ""
    led_rgb: Tuple[int, int, int] = (0, 255, 0)

    _packages: List[Package] = field(default_factory=list, repr=False)

    # -------------------------
    # Package handling
    # -------------------------
    @property
    def packages(self) -> List[Package]:
        """Return the robot's current packages."""
        return list(self._packages)

    @packages.setter
    def packages(self, val: List[Package]) -> None:
        """
        Replace all packages after validating constraints.

        Args:
            val: List of Package instances.
        """
        if not isinstance(val, list) or not all(isinstance(p, Package) for p in val):
            raise TypeError("packages must be a list[Package].")

        self._validate_package_constraints(val)
        self._packages = list(val)

    def add_package(self, pkg: Package) -> None:
        """
        Add a package to this robot while enforcing constraints.

        Args:
            pkg: Package instance to add.
        """
        if not isinstance(pkg, Package):
            raise TypeError("pkg must be a Package.")

        new_list = self._packages + [pkg]
        self._validate_package_constraints(new_list)
        self._packages.append(pkg)

    def remove_package(self, package_id: Any) -> bool:
        """
        Remove a package by id (if your Package has an id attribute).

        Args:
            package_id: The id to match against Package.id (or Package.package_id).

        Returns:
            True if removed, False otherwise.
        """
        for i, p in enumerate(self._packages):
            pid = getattr(p, "id", None)
            if pid is None:
                pid = getattr(p, "package_id", None)

            if pid == package_id:
                del self._packages[i]
                return True
        return False

    def clear_packages(self) -> None:
        """Remove all packages."""
        self._packages.clear()

    def count_large_packages(self) -> int:
        """Return number of large packages."""
        return sum(1 for p in self._packages if getattr(p, "size", None) == PackageSize.LARGE)

    def count_small_packages(self) -> int:
        """Return number of small packages."""
        return sum(1 for p in self._packages if getattr(p, "size", None) == PackageSize.SMALL)

    @staticmethod
    def _validate_package_constraints(pkgs: List[Package]) -> None:
        """
        Validate package constraints for a given list.

        Raises:
            ValueError if constraints are violated.
        """
        if len(pkgs) > MAX_NUM_OF_PACKAGES:
            raise ValueError(f"Too many packages: max {MAX_NUM_OF_PACKAGES}.")

        large = sum(1 for p in pkgs if getattr(p, "size", None) == PackageSize.LARGE)
        small = sum(1 for p in pkgs if getattr(p, "size", None) == PackageSize.SMALL)

        if large > MAX_NUM_OF_LARGE_PACKAGES:
            raise ValueError(f"Too many large packages: max {MAX_NUM_OF_LARGE_PACKAGES}.")
        if small > MAX_NUM_OF_SMALL_PACKAGES:
            raise ValueError(f"Too many small packages: max {MAX_NUM_OF_SMALL_PACKAGES}.")

        # In case PackageSize is missing or unknown, we do not hard-fail here;
        # but you could enforce strictness if required.

    # -------------------------
    # State helpers
    # -------------------------
    def set_led(self, r: int, g: int, b: int) -> None:
        """
        Set LED RGB values (0..255).

        Args:
            r, g, b: RGB values.
        """
        for name, v in (("r", r), ("g", g), ("b", b)):
            if not isinstance(v, int):
                raise TypeError(f"{name} must be int.")
            if v < 0 or v > 255:
                raise ValueError(f"{name} must be in [0..255].")

        self.led_rgb = (r, g, b)

    def set_battery(self, value: float) -> None:
        """
        Set battery status in percent [0..100].

        Args:
            value: Battery level.
        """
        if not _is_number(value):
            raise TypeError("battery_status must be a number.")
        self.battery_status = float(_clamp(float(value), 0.0, 100.0))

    # -------------------------
    # API serialization
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert robot state to a JSON-serializable dict.

        Notes:
            Package objects may not be JSON-serializable by default, so we try
            to use Package.to_dict() if available.

        Returns:
            Dictionary representing the robot state.
        """
        pkg_list: List[Any] = []
        for p in self._packages:
            if hasattr(p, "to_dict") and callable(getattr(p, "to_dict")):
                pkg_list.append(p.to_dict())
            else:
                # Fallback: best-effort minimal representation
                pkg_list.append(
                    {
                        "size": str(getattr(p, "size", "")),
                        "start": getattr(p, "start", None),
                        "destination": getattr(p, "destination", None),
                    }
                )

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
        }

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Update robot state from a dict (e.g., from an API request).

        Only known fields are updated; unknown fields are ignored.
        This method is intentionally forgiving to simplify frontend integration.

        Args:
            data: Dict of update values.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dict.")

        # Booleans
        for key in ("is_parked", "is_door_opened", "is_reversing", "is_charging"):
            if key in data and _is_bool(data[key]):
                setattr(self, key, data[key])

        # Battery
        if "battery_status" in data and _is_number(data["battery_status"]):
            self.set_battery(float(data["battery_status"]))

        # Message
        if "message" in data and isinstance(data["message"], str):
            self.message = data["message"]

        # LED
        if "led_rgb" in data and isinstance(data["led_rgb"], (list, tuple)) and len(data["led_rgb"]) == 3:
            r, g, b = data["led_rgb"]
            try:
                self.set_led(int(r), int(g), int(b))
            except Exception:
                # ignore invalid LED values
                pass
