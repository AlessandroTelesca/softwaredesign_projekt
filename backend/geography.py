"""
TODO: Docstring
"""
import osmnx as ox
import networkx as nx

def web_map():
    """
    Returns a web map of Karlsruhe.
    """
    place: str = "Karlsruhe, Baden-Württemberg, Germany"
    graph = ox.graph_from_place(place, network_type="train")
    pass