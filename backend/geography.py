"""
Map maker.
"""
import osmnx as ox
import networkx as nx
import folium
from geopandas import GeoDataFrame


def web_map():
    """
    Returns a web map of all railways of Karlsruhe.
    Has two layers; one for the railways, and one for the stations. Stations are circles.
    """
    features = get_tram_features()
    railway = features[0]
    station = features[1]

    railway = railway.explore(style_kwds={"weight": 3}, tooltip=[
                              "maxspeed", "railway", "name", "highspeed"])
    station = station.explore(m=railway, marker_kwds={"radius": 12, "fill": True}, style_kwds={
                              "color": "Red", "fill": "True"}, tooltip=["name", "description", "network", "note", "wheelchair"])
    
    #graph = ox.graph.graph_from_place("Karlsruhe, Baden-Württemberg, Germany")
    # TODO: Figure out how to display routes interactively?
    #return ox.convert.graph_to_gdfs(graph, nodes=False).explore()

    folium.LayerControl().add_to(railway)
    return railway


def get_tram_features() -> tuple[GeoDataFrame, GeoDataFrame]:
    """
    Returns the railway as well as the tram stations.
    """
    place: str = "Karlsruhe, Baden-Württemberg, Germany"
    railway = ox.features_from_place(place, tags={"railway": "rail"})
    station = ox.features_from_place(place, tags={"railway": "tram_stop"})

    #print(ox.features_from_point((8.43915, 48.80257), tags={"highway": "primary", "tram": "yes"}, dist=30000.0))
    return (railway, station)