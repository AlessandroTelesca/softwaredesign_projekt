"""
Map maker.
"""
import osmnx as ox
import networkx as nx
import folium

def web_map():
    """
    Returns a web map of all railways of Karlsruhe.
    Has two layers; one for the railways, and one for the stations. Stations are circles.
    """
    place: str = "Karlsruhe, Baden-Württemberg, Germany"
    railway = ox.features_from_place(place, tags={"railway": "rail"})
    station = ox.features_from_place(place, tags={"railway": "station"})

    railway = railway.explore(style_kwds={"weight": 3}, tooltip=["maxspeed", "railway", "name", "highspeed"])
    station = station.explore(m=railway, marker_kwds={"radius": 12, "fill": True}, style_kwds={"color": "Red", "fill": "True"}, tooltip=["name", "description"])

    folium.LayerControl().add_to(railway)
    return railway