import json
import os
import sys

from core.graph import TransitGraph
from core.algorithms import dijkstra, bfs, dfs
from ui.display import display_route, display_network_info
from ui.menu import prompt, ask_station, ask_algorithm, ask_city

DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")
CITY_FILES = ["mini_reseau.json", "paris.json", "bordeaux.json", "lille.json", "lyon.json"]