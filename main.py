import json
import os
import sys

from core.graph import TransitGraph
from core.algorithms import dijkstra, bfs, dfs
from ui.display import display_route, display_network_info
from ui.menu import prompt, ask_station, ask_algorithm, ask_city

DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")
CITY_FILES = ["mini_reseau.json", "paris.json", "bordeaux.json", "lille.json", "lyon.json"]

def load_json(path: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  ⚠  File not found: '{path}'")
    except json.JSONDecodeError as e:
        print(f"  ⚠  JSON error in '{path}': {e}")
    return None

def load_default_networks() -> dict:
    networks = {}
    for filename in CITY_FILES:
        path = os.path.join(DATA_DIR, filename)
        data = load_json(path)
        if data:
            networks[data["nom"]] = data
    return networks