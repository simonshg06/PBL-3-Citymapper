import json
import os
import sys

from core.graph import TransitGraph
from core.algorithms import dijkstra, bfs, dfs
from ui.display import display_route, display_network_info
from ui.menu import prompt, ask_station, ask_algorithm, ask_city