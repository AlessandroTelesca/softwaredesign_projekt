"""
Erzeugt eine animierte Route mit OSMnx und Folium.

- lädt ein Straßennetz für Karlsruhe
- berechnet die kürzeste Route zwischen Start und Ziel
- zeigt eine animierte rote Linie (AntPath) entlang der Route
- zeigt die Gesamtlänge der Route in km in einer Info-Box
- speichert die Karte als 'route_map.html'
"""

from pathlib import Path

import osmnx as ox
import folium
from folium.plugins import AntPath
from branca.element import Element

# Gebiet, aus dem das Straßennetz geladen wird
PLACE = "Karlsruhe, Baden-Württemberg, Germany"

# Start- und Zieladressen (kannst du ändern)
START = "Karlsruhe Hauptbahnhof, Germany"
END = "Karlsruhe Durlach Bahnhof, Germany"


def build_route_map(
    place: str = PLACE,
    start: str = START,
    end: str = END,
) -> folium.Map:
    """
    Erstellt eine Karte mit animierter Route zwischen zwei Adressen.
    """
    print(f"[1/4] Lade Straßennetz für: {place!r} ...")
    G = ox.graph_from_place(place, network_type="drive")

    print(f"[2/4] Geocodiere Start und Ziel ...")
    start_lat, start_lon = ox.geocode(start)
    end_lat, end_lon = ox.geocode(end)

    start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
    end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

    print(f"[3/4] Berechne kürzeste Route ...")
    route = ox.shortest_path(G, start_node, end_node, weight="length")

    # Koordinaten (lat, lon) der Route
    route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]

    # Route als GeoDataFrame (OSMnx 2.x)
    route_gdf = ox.routing.route_to_gdf(G, route, weight="length")
    total_m = float(route_gdf["length"].sum())
    total_km = total_m / 1000.0

    print(f"Gesamtlänge der Route: {total_km:.2f} km")
    print(f"[4/4] Baue Karte ...")

    m = folium.Map(
        location=[start_lat, start_lon],
        zoom_start=13,
        tiles="CartoDB positron",
    )

    # Graue statische Route als Hintergrund
    folium.PolyLine(
        route_coords,
        color="gray",
        weight=3,
        opacity=0.5,
    ).add_to(m)

    # Animierte rote Route (AntPath)
    AntPath(
        locations=route_coords,
        color="red",
        weight=5,
        opacity=0.9,
        dash_array=[10, 20],  # Muster
        delay=800,            # Geschwindigkeit der Animation (ms)
    ).add_to(m)

    # Startmarker
    folium.Marker(
        location=[start_lat, start_lon],
        popup=f"Start: {start}",
        icon=folium.Icon(color="green", icon="play"),
    ).add_to(m)

    # Zielmarker
    folium.Marker(
        location=[end_lat, end_lon],
        popup=f"Ziel: {end}",
        icon=folium.Icon(color="red", icon="flag"),
    ).add_to(m)

    # Einfache Info-Box oben rechts mit der Gesamtlänge
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
        Strecke: {total_km:.2f} km
    </div>
    """
    m.get_root().html.add_child(Element(info_html))

    return m