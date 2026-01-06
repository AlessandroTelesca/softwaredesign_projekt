"""
geography.py

Utilities for generating maps and routes for Karlsruhe using OSMnx and Folium.

This module provides:
- A map of tram-related OSM features (rail + tram stops).
- A route map (shortest path on a drivable street network) with an animated AntPath.

Notes:
- The route is computed on a street graph (network_type="drive"), not on tram tracks.
- Start/end are currently textual addresses resolved by OSMnx geocoding.
"""

from __future__ import annotations

import os
from typing import Optional

import osmnx as ox
import folium
from geopandas import GeoDataFrame
from folium.plugins import AntPath
from branca.element import Element


class Map:
    """
    Map generator for Karlsruhe.

    Supports:
    - Loading tram-related OSM features (railway + tram stops).
    - Computing a shortest route between two addresses and rendering a Folium map.
    - Returning the rendered map as HTML.

    Attributes:
        city: Place name used to download the network/OSM features.
        start: Start address used for geocoding.
        end: End address used for geocoding.
        route_color: Hex color used for the animated AntPath route.
    """

    city: str = "Karlsruhe, Baden-Württemberg, Germany"
    start: str = "Karlsruhe Hauptbahnhof, Germany"
    end: str = "Karlsruhe Durlach Bahnhof, Germany"
    route_color: str = "#d32f2f"

    def __init__(
        self,
        city: str = city,
        start: str = start,
        end: str = end,
        route_color: str = route_color,
        start_icon_path: Optional[str] = None,
        end_icon_path: Optional[str] = None,
    ) -> None:
        self.city = city
        self.start = start
        self.end = end
        self.route_color = route_color

        # If caller doesn't provide explicit icon paths, we default to the two provided stop icons.
        self.start_icon_path = start_icon_path
        self.end_icon_path = end_icon_path

    @staticmethod
    def _icons_dir() -> str:
        return os.path.join(os.path.dirname(__file__), "icons")

    @staticmethod
    def _resolve_icon_path(explicit_path: Optional[str], default_filename: str) -> Optional[str]:
        """
        Resolve an icon path.

        Priority:
        1) explicit_path if provided and exists
        2) backend/icons/<default_filename> if exists
        3) None (caller should fall back to default Folium marker)
        """
        if explicit_path:
            p = os.path.abspath(explicit_path)
            if os.path.exists(p):
                return p

        p = os.path.join(Map._icons_dir(), default_filename)
        return p if os.path.exists(p) else None

    @staticmethod
    def _add_marker(
        m: folium.Map,
        lat: float,
        lon: float,
        popup: str,
        icon_path: Optional[str],
        fallback_color: str,
        fallback_icon: str,
        icon_size: tuple[int, int] = (32, 32),
    ) -> None:
        """
        Add a marker using a custom PNG icon if available, otherwise use a Folium default icon.
        """
        if icon_path and os.path.exists(icon_path):
            custom = folium.CustomIcon(icon_image=icon_path, icon_size=icon_size)
            folium.Marker(location=[lat, lon], popup=popup, icon=custom).add_to(m)
        else:
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                icon=folium.Icon(color=fallback_color, icon=fallback_icon),
            ).add_to(m)

    def build_route_map(self) -> folium.Map:
        """
        Build a Folium map with an animated route between self.start and self.end.
        """
        print(f"[1/4] Load street network for: {self.city} ...")
        G = ox.graph_from_place(self.city, network_type="drive")

        print("[2/4] Geocode start and end...")
        start_lat, start_lon = ox.geocode(self.start)
        end_lat, end_lon = ox.geocode(self.end)

        start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

        print("[3/4] Compute shortest route...")
        route = ox.shortest_path(G, start_node, end_node, weight="length")
        route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]

        route_gdf = ox.routing.route_to_gdf(G, route, weight="length")
        total_m = float(route_gdf["length"].sum())
        total_km = total_m / 1000.0

        print(f"Total route length: {total_km:.2f} km")
        print("[4/4] Build map...")

        m = folium.Map(
            location=[start_lat, start_lon],
            zoom_start=13,
            tiles="CartoDB positron",
        )

        # Gray static route background
        folium.PolyLine(route_coords, color="gray", weight=3, opacity=0.5).add_to(m)

        # Animated route (official line color)
        AntPath(
            locations=route_coords,
            color=self.route_color,
            weight=5,
            opacity=0.9,
            dash_array=[10, 20],
            delay=800,
        ).add_to(m)

        # Use your provided stop icons
        start_icon = self._resolve_icon_path(self.start_icon_path, "StopBlue.png")
        end_icon = self._resolve_icon_path(self.end_icon_path, "StopOrange.png")

        self._add_marker(
            m,
            start_lat,
            start_lon,
            popup=f"Start: {self.start}",
            icon_path=start_icon,
            fallback_color="green",
            fallback_icon="play",
        )
        self._add_marker(
            m,
            end_lat,
            end_lon,
            popup=f"End: {self.end}",
            icon_path=end_icon,
            fallback_color="red",
            fallback_icon="flag",
        )

        # Info box
        info_html = f"""
        <div style="
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 9999;
            background-color: white;
            padding: 6px 10px;
            border-radius: 4px;
            box-shadow: 0 0 5px rgba(0,0,0,0.3);
            font-family: Arial, sans-serif;
            font-size: 12px;">
            Route Length: {total_km:.2f} km
        </div>
        """
        m.get_root().html.add_child(Element(info_html))

        return m

    def to_html(self) -> str:
        """
        Render the route map as an HTML string.
        """
        return self.build_route_map().get_root()._repr_html_()
