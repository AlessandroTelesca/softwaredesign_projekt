"""
Map maker for tram and railway features in Karlsruhe.

Uses:
- OSMnx to download OpenStreetMap data
- GeoPandas to handle the GeoDataFrames
- Folium to create an interactive web map
"""

from typing import Tuple
from pathlib import Path

import osmnx as ox
import folium
from geopandas import GeoDataFrame


# Standard-Ort: Karlsruhe
DEFAULT_PLACE = "Karlsruhe, Baden-Württemberg, Germany"


def get_tram_features(place: str = DEFAULT_PLACE) -> Tuple[GeoDataFrame, GeoDataFrame]:
    """
    Lädt Railway-Linien und Tram-Haltestellen für den angegebenen Ort.

    Parameters
    ----------
    place : str
        Ortsname, den OSMnx / Nominatim versteht.

    Returns
    -------
    railway : GeoDataFrame
        Alle Features mit railway = "rail".
    station : GeoDataFrame
        Alle Features mit railway = "tram_stop".
    """
    tags_rail = {"railway": "rail"}
    tags_stop = {"railway": "tram_stop"}

    railway = ox.features_from_place(place, tags_rail)
    station = ox.features_from_place(place, tags_stop)

    return railway, station


def web_map(place: str = DEFAULT_PLACE) -> folium.Map:
    """
    Erzeugt eine interaktive Webkarte mit:
    - Railway-Linien als Layer
    - Tram-Haltestellen als Punkte

    Parameters
    ----------
    place : str
        Ortsname für die Karte.

    Returns
    -------
    folium.Map
        Interaktive Karte.
    """
    railway, station = get_tram_features(place)

    # Karte auf den Mittelpunkt der Railway-Geometrien zentrieren
    center = railway.unary_union.centroid
    m = folium.Map(location=[center.y, center.x], zoom_start=12, tiles="CartoDB positron")

    # Layer: Railways
    folium.GeoJson(
        railway,
        name="Railways",
        style_function=lambda feature: {"weight": 3},
        tooltip=folium.GeoJsonTooltip(
            fields=[f for f in ["name", "railway", "maxspeed"] if f in railway.columns],
            aliases=["Name", "Railway", "Maxspeed"],
            localize=True,
        ),
    ).add_to(m)

    # Layer: Tram stops als Kreise
    if "geometry" in station.columns:
        for _, row in station.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue

            y, x = geom.centroid.y, geom.centroid.x
            popup_text = row.get("name") or "Tram stop"

            folium.CircleMarker(
                location=[y, x],
                radius=8,
                fill=True,
                color="red",
                fill_color="red",
                fill_opacity=0.8,
                popup=popup_text,
            ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m


def main() -> None:
    """
    Einstiegspunkt, wenn die Datei direkt ausgeführt wird.

    - baut die Webkarte für Karlsruhe
    - speichert sie als 'karlsruhe_tram_map.html' im backend-Ordner
    """
    place = DEFAULT_PLACE
    print(f"Lade OSM-Daten für: {place} ...")

    m = web_map(place)

    # Datei IMMER im backend-Ordner speichern (neben geography.py)
    output_path = Path(__file__).parent / "karlsruhe_tram_map.html"
    m.save(output_path)

    print(f"Fertig! Karte gespeichert unter:\n{output_path}")


if __name__ == "__main__":
    main()
