import json
import os
import sys

from core.graph import TransitGraph
from core.algorithms import dijkstra, bfs, dfs
from ui.display import display_route, display_network_info
from ui.menu import prompt, ask_station, ask_algorithm, ask_city

DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")
CITY_FILES = ["mini_reseau.json", "paris.json", "bordeaux.json", "lille.json", "lyon.json"]

def load_json(path: str) -> dict | None: # Load JSON data from a file, with error handling
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  ⚠  File not found: '{path}'")
    except json.JSONDecodeError as e:
        print(f"  ⚠  JSON error in '{path}': {e}")
    return None

def load_default_networks() -> dict: # Load all city networks from the data directory and return them as a dictionary
    networks = {}
    for filename in CITY_FILES:
        path = os.path.join(DATA_DIR, filename)
        data = load_json(path)
        if data:
            networks[data["nom"]] = data
    return networks

def plan_route(graph: TransitGraph): # Main function to plan a route between two stations using the selected algorithm
    print()
    departure = ask_station("Departure station", graph)
    arrival   = ask_station("Arrival station  ", graph)

    if departure == arrival:
        print("  ✘  Departure and arrival must be different.")
        return

    algo = ask_algorithm()

    if algo == "dijkstra":
        result = dijkstra(graph, departure, arrival)
        if result:
            path, cost = result
            display_route(path, cost, graph, "Dijkstra (fastest route)")
        else:
            print("  ✘  No path found.")

    elif algo == "bfs":
        result = bfs(graph, departure, arrival)
        if result:
            path, stops = result
            display_route(path, None, graph, f"BFS (fewest stops: {stops})")
        else:
            print("  ✘  No path found.")

    else:  # dfs
        result = dfs(graph, departure, arrival)
        if result:
            path, stops = result
            display_route(path, None, graph, f"DFS (depth-first, {stops} segments)")
        else:
            print("  ✘  No path found.")

    prompt("  Press Enter to continue…")



    SEP  = "─" * 60


def format_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    if m == 0:
        return f"{s}s"
    return f"{m} min {s}s" if s else f"{m} min"