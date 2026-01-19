"""
Singleton for the Flask backend.
Provides a global Simulation instance.

Adds: route simulation jobs that update robot.position + robot.progress smoothly,
and send status messages:
- ROUTE_TICK every 1 second
- ROUTE_PROGRESS every 5%
"""

from __future__ import annotations

import threading
from time import sleep
import time
import datetime as dt
from typing import Dict, List, Optional, Tuple

from backend.robot import Robot


def _haversine_m(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """
    Distance in meters between (lat,lon) points.
    """
    import math

    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    s = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(s), math.sqrt(1.0 - s))
    return R * c


def _resample_by_distance(coords: List[Tuple[float, float]], step_m: float) -> List[Tuple[float, float]]:
    """
    Create many points along the route with approx. equal spacing.
    This is what makes movement "constant speed" and smooth.
    """
    if not coords or len(coords) < 2:
        return coords

    step_m = float(step_m)
    if step_m <= 0:
        step_m = 10.0

    out: List[Tuple[float, float]] = [coords[0]]

    for i in range(len(coords) - 1):
        a = coords[i]
        b = coords[i + 1]
        dist = _haversine_m(a, b)
        if dist <= 0:
            continue

        n = int(dist // step_m)
        for k in range(1, n + 1):
            t = (k * step_m) / dist
            if t >= 1:
                break
            lat = a[0] + (b[0] - a[0]) * t
            lon = a[1] + (b[1] - a[1]) * t
            out.append((lat, lon))
        out.append(b)

    return out


def _cumdist(coords: List[Tuple[float, float]]) -> List[float]:
    """
    cumulative distance array in meters (same length as coords).
    """
    cum = [0.0]
    total = 0.0
    for i in range(len(coords) - 1):
        total += _haversine_m(coords[i], coords[i + 1])
        cum.append(total)
    return cum


def _interp_on_cum(coords: List[Tuple[float, float]], cum: List[float], target_m: float) -> Tuple[float, float]:
    """
    Linear interpolation of (lat,lon) for a target distance along the polyline.
    """
    if not coords:
        return (0.0, 0.0)
    if len(coords) == 1:
        return coords[0]

    # clamp
    if target_m <= 0:
        return coords[0]
    if target_m >= cum[-1]:
        return coords[-1]

    # find segment (linear scan is fine for student project; could be binary search)
    idx = 0
    for i in range(len(cum) - 1):
        if cum[i] <= target_m <= cum[i + 1]:
            idx = i
            break

    a = coords[idx]
    b = coords[idx + 1]
    d0 = cum[idx]
    d1 = cum[idx + 1]
    seg = d1 - d0
    if seg <= 0:
        return a

    t = (target_m - d0) / seg
    lat = a[0] + (b[0] - a[0]) * t
    lon = a[1] + (b[1] - a[1]) * t
    return (lat, lon)


class Simulation:
    """
    Simulation environment. Holds robots and simulated time.

    Also manages route jobs that move a robot along a route.
    """

    _seconds_per_tick: int = 1
    time_per_tick: int = 60
    _date_and_time: Optional[dt.datetime] = None
    _robots: List[Robot] = []
    _ticks: int = 0
    thread: Optional[threading.Thread] = None

    # route jobs
    _route_lock: threading.Lock
    _route_id_counter: int
    _route_threads: Dict[int, threading.Thread]

    def __init__(self, robots: List[Robot] = [], time_per_tick: int = 1):
        self._route_lock = threading.Lock()
        self._route_id_counter = 0
        self._route_threads = {}

        self.robots = robots
        self.seconds_per_tick = time_per_tick

        self.thread = threading.Thread(target=self.timer_ticks)
        self.thread.daemon = True
        self.thread.start()

    # -------------------------
    # Getters / Setters
    # -------------------------
    @property
    def date(self) -> str:
        return self.date_and_time.strftime("%d.%m.%y")

    @property
    def time(self) -> str:
        return self.date_and_time.strftime("%H:%M")

    @property
    def date_and_time(self) -> dt.datetime:
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
    def robots(self) -> List[Robot]:
        return self._robots

    @robots.setter
    def robots(self, robot: Robot = None):
        if robot:
            rbt = self.robots
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
        self._robots = []
        self._ticks = 0
        self._date_and_time = dt.datetime.now()

    def timer_ticks(self):
        while True:
            sleep(self.seconds_per_tick)
            self._ticks += 1
            new_time = self.date_and_time + dt.timedelta(0, seconds=self.time_per_tick)
            self._date_and_time = new_time

    # -------------------------
    # Route job (Backend-master)
    # -------------------------
    def start_route_job(
        self,
        robot_id: int,
        coords: List[Tuple[float, float]],
        duration_s: float,
        route_color: str = "#d32f2f",
    ) -> int:
        """
        Start a route simulation for robot_id. Returns route_id.

        The robot is updated smoothly (20Hz), but messages are sent:
        - every 1 second ROUTE_TICK
        - every 5% ROUTE_PROGRESS
        """
        robot = self._robots[robot_id]  # may raise IndexError

        if not coords or len(coords) < 2:
            raise ValueError("coords must contain at least 2 points")

        duration_s = float(duration_s)
        if duration_s <= 0:
            duration_s = 10.0

        # resample for constant speed look
        route_pts = _resample_by_distance(coords, step_m=12.0)
        cum = _cumdist(route_pts)
        total_m = cum[-1] if cum else 0.0
        if total_m <= 0:
            raise ValueError("route distance is zero")

        with self._route_lock:
            self._route_id_counter += 1
            route_id = self._route_id_counter

        def run():
            # init robot
            robot.is_parked = False
            robot.set_progress_position(0.0, route_pts[0][0], route_pts[0][1])
            robot.add_message("ROUTE_STARTED", "Route started.", 0.0)

            start_ts = time.time()

            last_tick_sec = -1
            last_progress_bucket = -1  # 5% steps => 0..20
            fps_sleep = 0.05  # 20Hz updates

            while True:
                now = time.time()
                elapsed = now - start_ts
                progress = min(1.0, max(0.0, elapsed / duration_s))

                # position from progress (distance-based)
                target_m = progress * total_m
                lat, lon = _interp_on_cum(route_pts, cum, target_m)
                robot.set_progress_position(progress, lat, lon)

                # ROUTE_TICK every 1s (stable)
                sec = int(elapsed)
                if sec != last_tick_sec:
                    last_tick_sec = sec
                    robot.add_message(
                        "ROUTE_TICK",
                        f"Route tick: t={sec}s, progress={int(progress*100)}%",
                        progress,
                    )

                # ROUTE_PROGRESS every 5%
                bucket = int((progress * 100.0) // 5)  # 0..20
                if bucket > last_progress_bucket:
                    last_progress_bucket = bucket
                    pct = min(100, bucket * 5)
                    robot.add_message("ROUTE_PROGRESS", f"{pct}% reached.", progress)

                if progress >= 1.0:
                    break

                sleep(fps_sleep)

            # finish
            robot.set_progress_position(1.0, route_pts[-1][0], route_pts[-1][1])
            robot.is_parked = True
            robot.add_message("ROUTE_FINISHED", "Route finished.", 1.0)

        t = threading.Thread(target=run, daemon=True)
        t.start()

        with self._route_lock:
            self._route_threads[route_id] = t

        return route_id
