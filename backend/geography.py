"""
geography.py

Route map generation using OSMnx + Folium.

- shortest path route between two addresses (drive network)
- grey base route (optional)
- animated "thermometer" fill (red) with constant speed (distance-based)
- moving vehicle marker:
    - default: red dot (circle marker)
    - optional: custom icon (lok.png) ONLY if enabled via JSON
- km info box (optional)
"""

from __future__ import annotations

import os
import json

import folium
import osmnx as ox
from branca.element import Element


class Map:
    CITY_DEFAULT = "Karlsruhe, Baden-Württemberg, Germany"

    def __init__(
        self,
        start: str,
        end: str,
        city: str = CITY_DEFAULT,
        route_color: str = "#d32f2f",
        animation_duration_s: float = 10.0,
        smooth_steps_per_segment: int = 16,
        show_grey: bool = True,
        show_km: bool = True,
        use_vehicle_icon: bool = False,  # 🔴 DEFAULT: red dot
    ) -> None:
        self.city = city
        self.start = start
        self.end = end

        self.route_color = route_color
        self.animation_duration_s = float(animation_duration_s)
        self.smooth_steps_per_segment = int(smooth_steps_per_segment)

        self.show_grey = bool(show_grey)
        self.show_km = bool(show_km)
        self.use_vehicle_icon = bool(use_vehicle_icon)

    @staticmethod
    def _icons_dir() -> str:
        return os.path.join(os.path.dirname(__file__), "icons")

    @staticmethod
    def _route_length_km(G, route) -> float:
        """
        Robust length calculation across OSMnx versions using route_to_gdf.
        """
        try:
            route_gdf = ox.routing.route_to_gdf(G, route, weight="length")
            total_m = float(route_gdf["length"].sum())
            return total_m / 1000.0
        except Exception:
            return 0.0

    def to_html(self) -> str:
        # 1) Load network
        G = ox.graph_from_place(self.city, network_type="drive")

        # 2) Geocode
        start_lat, start_lon = ox.geocode(self.start)
        end_lat, end_lon = ox.geocode(self.end)

        # 3) Nearest nodes
        start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

        # 4) Shortest path
        route = ox.shortest_path(G, start_node, end_node, weight="length")
        coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]

        total_km = self._route_length_km(G, route)

        # 5) Build map
        m = folium.Map(location=coords[0], zoom_start=13, tiles="CartoDB positron")

        # Grey base route (optional)
        if self.show_grey:
            folium.PolyLine(
                coords,
                color="gray",
                weight=4,
                opacity=0.45,
            ).add_to(m)

        # Start / End markers (stop icons)
        blue_stop = os.path.join(self._icons_dir(), "StopBlue.png")
        orange_stop = os.path.join(self._icons_dir(), "StopOrange.png")

        folium.Marker(
            [start_lat, start_lon],
            popup=f"Start: {self.start}",
            icon=folium.CustomIcon(blue_stop, icon_size=(32, 32))
            if os.path.exists(blue_stop)
            else folium.Icon(color="blue"),
        ).add_to(m)

        folium.Marker(
            [end_lat, end_lon],
            popup=f"End: {self.end}",
            icon=folium.CustomIcon(orange_stop, icon_size=(32, 32))
            if os.path.exists(orange_stop)
            else folium.Icon(color="orange"),
        ).add_to(m)

        # KM box (top-right)
        if self.show_km:
            info_html = f"""
            <div style="
                position: fixed;
                top: 10px;
                right: 10px;
                z-index: 99999;
                background-color: white;
                padding: 8px 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                font-family: Arial, sans-serif;
                font-size: 12px;">
                <b>Route Length</b><br/>
                {total_km:.2f} km
            </div>
            """
            m.get_root().html.add_child(Element(info_html))

        # 6) JS animation (constant speed, distance-based)
        route_js = json.dumps(coords)
        map_name = m.get_name()

        # smooth -> step meters mapping
        smooth = max(0, min(self.smooth_steps_per_segment, 50))
        step_m = max(5, min(40, int(round(35 - smooth * 1.5))))

        duration_s = max(1.0, min(self.animation_duration_s, 60.0))

        # vehicle icon exists?
        lok_path_abs = os.path.join(self._icons_dir(), "lok.png")
        lok_exists = os.path.exists(lok_path_abs)

        # HTML is saved into backend/ -> relative path to backend/icons/
        lok_rel = "icons/lok.png"

        animation_block = f"""
        <script>
        (function() {{
          window.addEventListener("load", function() {{
            try {{
              var rawRoute = {route_js};
              var map = {map_name};

              if (typeof L === "undefined" || !map || !rawRoute || rawRoute.length < 2) {{
                console.warn("Animation prerequisites missing.");
                return;
              }}

              function resampleByDistance(route, stepMeters) {{
                var out = [];
                out.push(route[0]);

                for (var i = 0; i < route.length - 1; i++) {{
                  var a = L.latLng(route[i][0], route[i][1]);
                  var b = L.latLng(route[i+1][0], route[i+1][1]);
                  var dist = map.distance(a, b);
                  if (dist <= 0) continue;

                  var n = Math.floor(dist / stepMeters);
                  for (var k = 1; k <= n; k++) {{
                    var t = (k * stepMeters) / dist;
                    if (t >= 1) break;
                    var lat = a.lat + (b.lat - a.lat) * t;
                    var lng = a.lng + (b.lng - a.lng) * t;
                    out.push([lat, lng]);
                  }}
                  out.push([b.lat, b.lng]);
                }}

                return out;
              }}

              var stepMeters = {step_m};
              var route = resampleByDistance(rawRoute, stepMeters);

              // cumulative distances
              var cum = [0];
              var total = 0;
              for (var i = 0; i < route.length - 1; i++) {{
                var p1 = L.latLng(route[i][0], route[i][1]);
                var p2 = L.latLng(route[i+1][0], route[i+1][1]);
                total += map.distance(p1, p2);
                cum.push(total);
              }}

              var durationMs = {duration_s} * 1000;

              // red progressive line
              var polyline = L.polyline([], {{
                color: "{self.route_color}",
                weight: 5,
                opacity: 0.95,
                smoothFactor: 1.0
              }}).addTo(map);

              // ✅ DEFAULT is RED DOT
              // Icon only if explicitly enabled AND file exists
              var useIcon = {str(self.use_vehicle_icon).lower()} && {str(lok_exists).lower()};
              var vehicle;

              if (useIcon) {{
                var vehicleIcon = L.icon({{
                  iconUrl: "{lok_rel}",
                  iconSize: [32, 32],
                  iconAnchor: [16, 16]
                }});
                vehicle = L.marker(route[0], {{
                  icon: vehicleIcon,
                  interactive: false
                }}).addTo(map);
              }} else {{
                vehicle = L.circleMarker(route[0], {{
                  radius: 6,
                  color: "black",
                  weight: 2,
                  fillColor: "{self.route_color}",
                  fillOpacity: 1
                }}).addTo(map);
              }}

              var lastIndex = 0;
              polyline.addLatLng(route[0]);

              function findIndexForDistance(d) {{
                for (var i = 0; i < cum.length - 1; i++) {{
                  if (d >= cum[i] && d <= cum[i+1]) return i;
                }}
                return cum.length - 2;
              }}

              var startTs = null;

              function frame(ts) {{
                if (startTs === null) startTs = ts;
                var elapsed = ts - startTs;
                var progress = Math.min(1, elapsed / durationMs);
                var targetDist = progress * total;

                var idx = findIndexForDistance(targetDist);

                while (lastIndex < idx) {{
                  lastIndex++;
                  polyline.addLatLng(route[lastIndex]);
                }}

                var segStart = L.latLng(route[idx][0], route[idx][1]);
                var segEnd = L.latLng(route[idx+1][0], route[idx+1][1]);

                var segFrom = cum[idx];
                var segTo = cum[idx+1];
                var within = (segTo - segFrom) > 0 ? (targetDist - segFrom) / (segTo - segFrom) : 0;
                within = Math.max(0, Math.min(1, within));

                var lat = segStart.lat + (segEnd.lat - segStart.lat) * within;
                var lng = segStart.lng + (segEnd.lng - segStart.lng) * within;

                vehicle.setLatLng([lat, lng]);

                if (progress < 1) {{
                  window.requestAnimationFrame(frame);
                }} else {{
                  // finish
                  if (lastIndex < route.length - 1) {{
                    for (var j = lastIndex + 1; j < route.length; j++) {{
                      polyline.addLatLng(route[j]);
                    }}
                  }}
                  vehicle.setLatLng(route[route.length - 1]);
                }}
              }}

              window.requestAnimationFrame(frame);

            }} catch (e) {{
              console.error("Route animation error:", e);
            }}
          }});
        }})();
        </script>
        """
        m.get_root().html.add_child(Element(animation_block))

        return m.get_root().render()
