"""
Map maker.
"""
import osmnx as ox
import networkx as nx

def web_map():
    """
    Returns a web map of all railways of Karlsruhe.
    """
    place: str = "Karlsruhe, Baden-Württemberg, Germany"
    graph = ox.graph_from_place(place, custom_filter="['railway'~'tram|rail']")
    return ox.convert.graph_to_gdfs(graph, nodes=False).explore()