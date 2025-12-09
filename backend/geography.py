"""
Map maker.
"""
import osmnx as ox
import networkx as nx
import folium
from geopandas import GeoDataFrame


class Map:
    start: str = "Karlsruhe Hauptbahnhof, Germany"
    end: str = "Karlsruhe Durlach Bahnhof, Germany"
    city: str = "Karlsruhe, Baden-Württemberg, Germany"

    def __init__(self, city: str, start: str = start, end: str = end):
        """
        TODO: Docstring
        """
        self.city = city
        self.start = start
        self.end = end
    

    def compute_route_coords(self, start: str = None, end: str = None):
        """
        Berechnet die Route und gibt eine Liste (lat, lon)-Koordinaten zurück.
        """
        if start is None:
            start = self.start
        if end is None:
            end = self.end
        print(f"[1/3] Lade Straßennetz für: {self.city} ...")
        G = ox.graph_from_place(self.city, network_type="drive")

        print("[2/3] Geocodiere Start und Ziel ...")
        start_lat, start_lon = ox.geocode(self.start)
        end_lat, end_lon = ox.geocode(self.end)

        start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

        print("[3/3] Berechne kürzeste Route ...")
        route = ox.shortest_path(G, start_node, end_node, weight="length")

        coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]
        return coords
    
    
    def web_map(self):
        """
        Returns a web map of all railways of Karlsruhe.
        Has two layers; one for the railways, and one for the stations. Stations are circles.
        """
        features = Map.get_tram_features()
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

    @staticmethod
    def get_tram_features() -> tuple[GeoDataFrame, GeoDataFrame]:
        """
        Returns the railway as well as the tram stations.
        """
        place: str = "Karlsruhe, Baden-Württemberg, Germany"
        railway = ox.features_from_place(place, tags={"railway": "rail"})
        station = ox.features_from_place(place, tags={"railway": "tram_stop"})

        #print(ox.features_from_point((8.43915, 48.80257), tags={"highway": "primary", "tram": "yes"}, dist=30000.0))
        return railway, station


class ToString:
    """
    TODO: Docstring
    """
    def __init__(self, text: str):
        """
        TODO: Docstring
        """