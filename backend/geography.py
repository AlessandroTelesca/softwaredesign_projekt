"""
geography.py

Route map generation using OSMnx + Folium.

Two modes:
A) robot_id is None -> classic client-side animation (distance-based, smooth)
B) robot_id is given -> "Backend-master": robot position is simulated in backend,
   map polls /api/robot/read and interpolates smoothly to avoid jumps/ruckeln.

lok.png / vehicle icon is REMOVED (always red dot).
"""

from __future__ import annotations

import json
import os
from typing import Optional

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
        show_grey: bool = True,
        show_km: bool = True,
        robot_id: Optional[int] = None,  # if set => polling backend robot state
    ) -> None:
        self.city = city
        self.start = start
        self.end = end
        self.route_color = route_color
        self.animation_duration_s = float(animation_duration_s)
        self.show_grey = bool(show_grey)
        self.show_km = bool(show_km)
        self.robot_id = robot_id

    @staticmethod
    def _icons_dir() -> str:
        return os.path.join(os.path.dirname(__file__), "icons")

    @staticmethod
    def _route_length_km(G, route) -> float:
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
            folium.PolyLine(coords, color="gray", weight=4, opacity=0.45).add_to(m)

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

        # 6) Animation JS
        route_js = json.dumps(coords)
        map_name = m.get_name()

        # Mode A: classic animation (no backend polling)
        if self.robot_id is None:
            duration_s = max(1.0, min(self.animation_duration_s, 60.0))
            animation_block = f"""
            <script>
            (function() {{
              window.addEventListener("load", function() {{
                try {{
                  var rawRoute = {route_js};
                  var map = {map_name};
                  if (!map || !rawRoute || rawRoute.length < 2 || typeof L === "undefined") return;

                  // resample by distance for constant speed
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

                  var route = resampleByDistance(rawRoute, 12);

                  // cumulative distance
                  var cum = [0];
                  var total = 0;
                  for (var i = 0; i < route.length - 1; i++) {{
                    total += map.distance(L.latLng(route[i][0], route[i][1]), L.latLng(route[i+1][0], route[i+1][1]));
                    cum.push(total);
                  }}

                  var polyline = L.polyline([], {{ color: "{self.route_color}", weight: 5, opacity: 0.95 }}).addTo(map);
                  var vehicle = L.circleMarker(route[0], {{
                    radius: 6, color: "black", weight: 2,
                    fillColor: "{self.route_color}", fillOpacity: 1
                  }}).addTo(map);

                  polyline.addLatLng(route[0]);
                  var lastIndex = 0;
                  var durationMs = {duration_s} * 1000;
                  var startTs = null;

                  function findIndexForDistance(d) {{
                    for (var i = 0; i < cum.length - 1; i++) {{
                      if (d >= cum[i] && d <= cum[i+1]) return i;
                    }}
                    return cum.length - 2;
                  }}

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

                    if (progress < 1) requestAnimationFrame(frame);
                    else {{
                      vehicle.setLatLng(route[route.length - 1]);
                    }}
                  }}

                  requestAnimationFrame(frame);

                }} catch(e) {{
                  console.error(e);
                }}
              }});
            }})();
            </script>
            """
            m.get_root().html.add_child(Element(animation_block))
            return m.get_root().render()

        # Mode B: Backend-master (poll robot state + interpolate)
        robot_id = int(self.robot_id)

        polling_block = f"""
        <script>
        (function() {{
          window.addEventListener("load", function() {{
            var map = {map_name};
            var rawRoute = {route_js};
            if (!map || !rawRoute || rawRoute.length < 2 || typeof L === "undefined") return;

            // Build a resampled route for drawing and for progress->position mapping
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

            var route = resampleByDistance(rawRoute, 12);

            // cumulative distances for mapping progress->position
            var cum = [0];
            var total = 0;
            for (var i = 0; i < route.length - 1; i++) {{
              total += map.distance(L.latLng(route[i][0], route[i][1]), L.latLng(route[i+1][0], route[i+1][1]));
              cum.push(total);
            }}

            function posFromProgress(p) {{
              p = Math.max(0, Math.min(1, p));
              var target = p * total;

              // find segment
              var idx = 0;
              for (var i = 0; i < cum.length - 1; i++) {{
                if (target >= cum[i] && target <= cum[i+1]) {{ idx = i; break; }}
              }}

              var segFrom = cum[idx];
              var segTo = cum[idx+1];
              var within = (segTo - segFrom) > 0 ? (target - segFrom) / (segTo - segFrom) : 0;
              within = Math.max(0, Math.min(1, within));

              var a = L.latLng(route[idx][0], route[idx][1]);
              var b = L.latLng(route[idx+1][0], route[idx+1][1]);
              var lat = a.lat + (b.lat - a.lat) * within;
              var lng = a.lng + (b.lng - a.lng) * within;
              return [lat, lng];
            }}

            // Draw progressive red line (thermometer fill)
            var polyline = L.polyline([], {{
              color: "{self.route_color}", weight: 5, opacity: 0.95
            }}).addTo(map);

            // Vehicle marker (always red dot)
            var vehicle = L.circleMarker(route[0], {{
              radius: 6, color: "black", weight: 2,
              fillColor: "{self.route_color}", fillOpacity: 1
            }}).addTo(map);

            // Interpolation state
            var targetProgress = 0.0;
            var shownProgress = 0.0;
            var lastPollTs = performance.now();

            // Avoid backward jumps
            function setTarget(p) {{
              p = Math.max(0, Math.min(1, p));
              if (p < targetProgress) return;
              targetProgress = p;
            }}

            // Poll backend frequently (smooth), but backend messages remain 1s/5%
            async function poll() {{
              try {{
                var resp = await fetch("/api/robot/read?robot_id={robot_id}", {{ cache: "no-store" }});
                if (!resp.ok) throw new Error("poll failed");
                var data = await resp.json();
                var st = data && data.status ? data.status : null;
                if (st && typeof st.progress === "number") {{
                  setTarget(st.progress);
                }}
              }} catch (e) {{
                // ignore temporary errors
              }} finally {{
                setTimeout(poll, 250);
              }}
            }}
            poll();

            // Rendering loop: move smoothly towards targetProgress
            var lastFrame = performance.now();
            function frame(now) {{
              var dt = (now - lastFrame) / 1000.0;
              lastFrame = now;

              // speed limiter: how fast progress can change per second (prevents "too fast at start")
              // This makes the visible motion stable even if the first poll arrives late.
              var maxDelta = 0.06 * dt; // ~6% per second max
              var diff = targetProgress - shownProgress;
              if (diff > maxDelta) diff = maxDelta;
              if (diff < 0) diff = 0;

              shownProgress = Math.min(1.0, shownProgress + diff);

              // update vehicle position and progressive line
              var pos = posFromProgress(shownProgress);
              vehicle.setLatLng(pos);

              // fill line based on shownProgress
              var idx = Math.floor(shownProgress * (route.length - 1));
              if (idx < 0) idx = 0;
              if (idx >= route.length) idx = route.length - 1;

              // reset polyline points cheaply
              var pts = [];
              for (var i = 0; i <= idx; i++) pts.push(route[i]);
              polyline.setLatLngs(pts);

              requestAnimationFrame(frame);
            }}
            requestAnimationFrame(frame);
          }});
        }})();
        </script>
        """

        m.get_root().html.add_child(Element(polling_block))
        return m.get_root().render()
