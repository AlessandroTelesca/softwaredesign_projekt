"""
Map maker.
"""
from tracemalloc import start
import osmnx as ox
import networkx as nx
import folium
from geopandas import GeoDataFrame
from folium.plugins import AntPath
from branca.element import Element


class Map:
    """
    TODO: Docstring
    TODO: Dennisé: Make the code cleaner and document it properly. Use the README.md for this.
    TODO: Dennisé: Add a possibility for the frontend to set start and end. This is an API call for the middleware.
    TODO: Dennisé: Add all possible tramways; refer yourself to the SoftwareDesign specification within the Felix course (Materialordner > KVV_Lines_v2.json).
    TODO: Dennisé: I added the stop markers within icons/. Would be cool if you changed the Folium markers to them.
    TODO: Dennisé: It would be nice to have the colour of the ant map correspond to the colour of the official tram lines. Check Materialordner > KVV-Linien-Icons.zip for them. Add them in icons/.
    """
    city: str = "Karlsruhe, Baden-Württemberg, Germany"
    start: str = "Karlsruhe Hauptbahnhof, Germany"
    end: str = "Karlsruhe Durlach Bahnhof, Germany"
    
    def __init__(self, city: str = city, start: str = start, end: str = end):
        self.city = city
        self.start = start
        self.end = end

    def compute_route_coords(self, start: str = None, end: str = None):
        """
        Computes the route and returns a list of (lat, lon) coordinates.
        """
        if start is None:
            start = self.start
        if end is None:
            end = self.end
        print(f"[1/3] Load street network for: {self.city} ...")
        G = ox.graph_from_place(self.city, network_type="drive")

        print("[2/3] Geocode start and end...")
        start_lat, start_lon = ox.geocode(self.start)
        end_lat, end_lon = ox.geocode(self.end)

        start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

        print("[3/3] Compute shortest route...")
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

        # graph = ox.graph.graph_from_place("Karlsruhe, Baden-Württemberg, Germany")
        # TODO: Figure out how to display routes interactively?
        # return ox.convert.graph_to_gdfs(graph, nodes=False).explore()

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

        return railway, station

    def build_route_map(self) -> folium.Map:
        """
        Builds a map with an animated route between two addresses.
        """
        print(f"[1/4] Load street network for: {self.city} ...")
        G = ox.graph_from_place(self.city, network_type="drive")

        print(f"[2/4] Geocode start and end...")
        start_lat, start_lon = ox.geocode(self.start)
        end_lat, end_lon = ox.geocode(self.end)

        start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

        print(f"[3/4] Compute shortest route...")
        route = ox.shortest_path(G, start_node, end_node, weight="length")

        # Coordinates (lat, lon) of the route
        route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]

        # Route as GeoDataFrame (OSMnx 2.x)
        route_gdf = ox.routing.route_to_gdf(G, route, weight="length")
        total_m = float(route_gdf["length"].sum())
        total_km = total_m / 1000.0

        print(f"Total route length: {total_km:.2f} km")
        print(f"[4/4] Build map...")

        m = folium.Map(
            location=[start_lat, start_lon],
            zoom_start=13,
            tiles="CartoDB positron",
        )

        # Gray static route as background
        folium.PolyLine(
            route_coords,
            color="gray",
            weight=3,
            opacity=0.5,
        ).add_to(m)

        # Animated red route (AntPath)
        AntPath(
            locations=route_coords,
            color="red",
            weight=5,
            opacity=0.9,
            dash_array=[10, 20],  # Pattern
            delay=800,            # Animation speed (ms)
        ).add_to(m)

        # Start marker
        folium.Marker(
            location=[start_lat, start_lon],
            popup=f"Start: {self.start}",
            icon=folium.Icon(color="green", icon="play"),
        ).add_to(m)

        # End marker
        folium.Marker(
            location=[end_lat, end_lon],
            popup=f"End: {self.end}",
            icon=folium.Icon(color="red", icon="flag"),
        ).add_to(m)

        # Simple info box at the top right with the total length
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
            Route Length: {total_km:.2f} km
        </div>
        """
        m.get_root().html.add_child(Element(info_html))

        return m

    def to_html(self) -> str:
        """
        Returns the map as an HTML string.
        """
        web_map = self.build_route_map().get_root()._repr_html_()
        return web_map