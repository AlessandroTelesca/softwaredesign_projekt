"""
Berechnet eine Route mit OSMnx und erzeugt eine HTML-Datei
mit Leaflet-JavaScript, die:

- die Route grau darstellt
- einen roten Punkt entlang der Route fahren lässt
- die rote Linie Stück für Stück aufbaut

Ergebnis: route_animation.html im gleichen Ordner wie dieses Skript.
"""

from pathlib import Path
import json

import osmnx as ox

# Gebiet und Adressen
PLACE = "Karlsruhe, Baden-Württemberg, Germany"
START = "Karlsruhe Hauptbahnhof, Germany"
END = "Karlsruhe Durlach Bahnhof, Germany"


def compute_route_coords(start: str = START, end: str = END):
    """
    Berechnet die Route und gibt eine Liste (lat, lon)-Koordinaten zurück.
    """
    print(f"[1/3] Lade Straßennetz für: {PLACE!r} ...")
    G = ox.graph_from_place(PLACE, network_type="drive")

    print("[2/3] Geocodiere Start und Ziel ...")
    start_lat, start_lon = ox.geocode(START)
    end_lat, end_lon = ox.geocode(END)

    start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
    end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

    print("[3/3] Berechne kürzeste Route ...")
    route = ox.shortest_path(G, start_node, end_node, weight="length")

    coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]
    return coords


def build_html(route_coords):
    """
    Erzeugt den HTML-String mit Leaflet und der Animation.
    """
    # JSON für JavaScript (Liste von [lat, lon])
    route_json = json.dumps(route_coords)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <title>Routenanimation</title>
  <link rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>
  <style>
    html, body, #map {{
      height: 100%;
      width: 100%;
      margin: 0;
      padding: 0;
    }}
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
          integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
          crossorigin=""></script>
  <script>
    // Koordinaten der Route aus Python
    var routeCoords = {route_json};

    if (!routeCoords || routeCoords.length === 0) {{
      alert("Keine Routenkoordinaten vorhanden.");
    }} else {{
      // Karte initialisieren
      var map = L.map('map').setView(routeCoords[0], 13);
      L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap-Mitwirkende'
      }}).addTo(map);

      // Graue Hintergrundroute
      L.polyline(routeCoords, {{
        color: 'gray',
        weight: 3,
        opacity: 0.5
      }}).addTo(map);

      // Rote Linie, die nach und nach wächst
      var filledLine = L.polyline([], {{
        color: 'red',
        weight: 5,
        opacity: 0.9
      }}).addTo(map);

      // Fahrender Marker
      var vehicle = L.circleMarker(routeCoords[0], {{
        radius: 6,
        color: 'red',
        fillColor: 'red',
        fillOpacity: 1.0
      }}).addTo(map);

      var i = 0;
      var maxIndex = routeCoords.length;

      function step() {{
        if (i >= maxIndex) {{
          return; // Animation fertig
        }}

        var coord = routeCoords[i];
        filledLine.addLatLng(coord);
        vehicle.setLatLng(coord);

        i += 1;

        // Geschwindigkeit der Animation (ms) – kleiner = schneller
        setTimeout(step, 150);
      }}

      step(); // Animation starten
    }}
  </script>
</body>
</html>
"""
    return html