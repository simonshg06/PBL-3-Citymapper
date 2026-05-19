import json # json reads the city files
import os # os handles file paths
import sys # sys is used for command-line arguments and exiting the program

from core.graph import TransitGraph 
from core.algorithms import dijkstra, bfs, dfs
from ui.display import display_route, display_network_info
from ui.menu import prompt, ask_station, ask_algorithm, ask_city

DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")
 #.dirname removes the filename from the path, then .join adds "data" to the path, giving us the full path to the data folder regardless of where the script is run from
CITY_FILES = ["mini_reseau.json", "paris.json", "bordeaux.json", "lille.json", "lyon.json"]
 # list of Json file names to load from the data directory. each file should contain a city's transit network in the expected format (with "nom", "lignes", etc.)

def load_json(path: str) -> dict | None: # the function takes a file path as input and expects to return a dictionary
    try: # attempts to run the code underneath
        with open(path, encoding="utf-8") as f: 
            # path tells us which file to open, and encoding="utf-8" ensures we can read special characters in station names without errors
            return json.load(f) # turns the json file into a python dictionary
    except FileNotFoundError: #the file doesn't exist at the given path, we catch that specific error and print a warning instead of crashing
        print(f"  ⚠  File not found: '{path}'") 
    except json.JSONDecodeError as e: # the file exists but contains invalid JSON, we catch that error and print a warning with the error message
        print(f"  ⚠  JSON error in '{path}': {e}")
    return None # return none if there was an error

def load_default_networks() -> dict: # Load all city networks from the data directory and return them as a dictionary
    networks = {} # empty dict to hold the loaded networks, indexed by city name
    for filename in CITY_FILES: # loop through each expected city file name
        path = os.path.join(DATA_DIR, filename) # builds the full file path by joining the data directory path with the filename
        data = load_json(path) # reads the json file and returns a dictionary
        if data: # if the data was loaded successfully
            networks[data["nom"]] = data 
            # we take the "nom" field from the data (which should be the city name) and use it as the key to store the entire network data in the networks dictionary
    return networks

def plan_route(graph: TransitGraph): # Main function to plan a route between two stations using the selected algorithm
    print() # just a blank line for spacing before the prompts start
    departure = ask_station("Departure station", graph) #calls ask station to prompt the user for a departure station 
    arrival   = ask_station("Arrival station  ", graph) #calls ask station to prompt the user for an arrival station

    if departure == arrival: 
        # if the user accidentally entered the same station for both departure and arrival, we catch that and print a warning instead of trying to find a route
        print("  ✘  Departure and arrival must be different.")
        return

    algo = ask_algorithm() # prompts the user to choose which algorithm they want to use for route planning (dijkstra, bfs, or dfs)

    if algo == "dijkstra": 
        result = dijkstra(graph, departure, arrival) 
        # calls the dijkstra function from core.algorithms, passing in the graph and the chosen departure and arrival stations.
        if result: # if dijkstra returns a valid result (a path and its total cost), we unpack it into path and cost variables
            path, cost = result 
            display_route(path, cost, graph, "Dijkstra (fastest route)") # displays the route usin the display route function
        else:
            print("  ✘  No path found.")

    elif algo == "bfs":  
        result = bfs(graph, departure, arrival)
          # calls the bfs function from core.algorithms, passing in the graph and the chosen departure and arrival stations.
        if result:  # if bfs returns a valid result (a path and the number of stops), we unpack it into path and stops variables
            path, stops = result 
            display_route(path, None, graph, f"BFS (fewest stops: {stops})") 
             # displays the route without a total cost but includes the number of stops in the algorithm name for clarity
        else:
            print("  ✘  No path found.")

    else:  # dfs
        result = dfs(graph, departure, arrival)
         # calls the dfs function from core.algorithms, passing in the graph and the chosen departure and arrival stations.
        if result:
            path, stops = result
            display_route(path, None, graph, f"DFS (depth-first, {stops} segments)")
             # displays the route without a cost again but indicates that it's a depth-first search and shows the number of stops (edges) in the path
        else:
            print("  ✘  No path found.")

    prompt("  Press Enter to continue…")





# Entry function for the program; accepts optional extra city networks as a dict
def run(extra_networks: dict | None = None):

    networks = load_default_networks()          # Load built-in city data from the data/ folder

    if extra_networks:
        networks.update(extra_networks)         # Merge any extra networks passed in (e.g. via --json flag)

    if not networks:
        print("  ✘  No city data found. Add JSON files to the data/ folder.")
        sys.exit(1)                             # Abort early — nothing to work with

    city_names = list(networks.keys())

    while True:                                 # Outer loop: keeps returning to city selection
        os.system("cls" if os.name == "nt" else "clear")  # Clear terminal (cls on Windows, clear on Unix)
        print("=" * 60)
        print("     🚇  TRANSIT ROUTE PLANNER  — ESME PBL")
        print("=" * 60)


        choice = ask_city(city_names, networks) # Show city picker; returns chosen city name, None, or ""

        if choice is None:                      # User explicitly chose Quit from city menu
            print("\n  Goodbye! 👋\n")
            break                               # Exit the outer while loop → program ends

        if not choice:                          # Empty string = invalid input, skip and re-prompt
            continue


        graph = TransitGraph(networks[choice])  # Build the graph structure for the selected city
        display_network_info(graph)             # Show stats (stations, lines, etc.) right after picking

        while True:                             # Inner loop: stays inside one city until user leaves
            print(f"\n  [City: {choice}]")
            print("  r) Plan a route")
            print("  i) Network info")
            print("  c) Change city")
            print("  q) Quit")


            action = prompt("\n  > ").lower()   # Read user input, normalise to lowercase

            if action == "q":
                print("\n  Goodbye! 👋\n")
                sys.exit(0)                     # Hard exit from anywhere in the inner menu

            elif action == "c":
                break                           # Break inner loop → falls back to outer city-picker loop

            elif action == "i":
                display_network_info(graph)     # Re-display network stats on demand

            elif action == "r":
                plan_route(graph)               # Launch the route-planning flow for this city

   
   

# Only runs when the script is executed directly (not imported as a module)
if __name__ == "__main__":
    extra = {}                                  # Will hold any city networks loaded via --json flags
    args  = sys.argv[1:]                        # Grab all command-line arguments after the script name
    i     = 0

    while i < len(args):                        # Walk through args manually (not using argparse)
        if args[i] == "--json" and i + 1 < len(args):  # Expect a filename immediately after --json
            data = load_json(args[i + 1])       # Parse the JSON file at the given path
            if data:
                extra[data["nom"]] = data       # Index the network by its city name ("nom" key)
                print(f"  Loaded extra network: {data['nom']}")
            i += 2                              # Skip both "--json" and the filename
        else:
            i += 1                              # Unknown flag — skip it silently

    run(extra)                                  # Kick off the program (note: original code has Run(extra) — capitalisation bug)