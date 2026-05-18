# PBL-3-Citymapper


#Presentation:
#-no code and +++ demo
#- 7min

# **📦 \[Project Name]**

Transit Route Planner

**MVP Status:** 

v1.0-Production

**Group Members:** 

Yousef Abouturkia, Charlie Delecour, Simon Berger


## **🎯 Project Overview**

Transit Route Planner is an interactive terminal app that lets you find the best route between two stations across several French city networks. You pick a city, enter where you're coming from and where you're going, and the app calculates your route using one of three algorithms.
Key Features:

   - Route planning across multiple French cities (Paris, Lyon, Bordeaux, Lille)
   - Three different algorithms to find your route depending on what matters to you
   - Transfer detection: the app tells you exactly where to change lines
   - Network stats for each city (number of lines, stations, transfer hubs)
   - Load your own custom city network via a JSON file from the command line

## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**\
   git clone (https://github.com/simonshg06/PBL-3-Citymapper.git)
cd PBL3-Citymapper

2. **Setup Virtual Environment:**\
   python -m venv .venv
source .venv/bin/activate  

3. **Install Dependencies:**\
   pip install -r requirements.txt

4. **Run Application:**\
   python main.py


## **🛠️ Technical Architecture**

Explain how your code is organized. An "Architect-level" README should describe the separation of concerns.

The code is split into four main modules with clear separation of concerns:


# 1 core/graph.py — The Network Graph

Purpose: Loads a city's JSON data and builds a graph out of it so the algorithms can navigate it.
How it works:

   - Every station on every line becomes its own node, written as StationName::LineID (e.g. Châtelet::1). This way the same station on two different lines is treated as two separate nodes.
   - Edges connect consecutive stations on the same line ("travel" edges) and connect different lines at the same station ("transfer" edges), each with a travel time in seconds.
   - If no explicit connection times are in the JSON, a default average time is used.

Key Methods:

   - start_nodes(station) --> returns all nodes for a given departure station (one per line)
   - end_nodes(station) --> same but as a set, used to quickly check if we've arrived
   - all_stations() --> sorted list of every station in the network
   - transfer_stations() --> stations served by more than one line
   - is_connected() --> checks that every node in the graph can be reached


# 2 core/algorithms.py — Route Finding

Purpose: Three algorithms that each find a path through the graph in a different way.

   - Fastest Route: finds the fastest route by minimising total travel time. Uses a priority queue so it always explores the cheapest option first.
   - BFS (Breadth-First Search): finds the route with the fewest stops, exploring station by station outward from the departure.
   - DFS (Depth-First Search): explores one path as far as it can go before backtracking. Doesn't guarantee the shortest or fastest route, but finds a valid path.




# 3 ui/display.py — Output Formatting

Purpose: Prints the route and network info in a clean, readable format in the terminal.

   - display_route(): prints the full journey step by step, showing where you board, where you transfer, and where you get off. Also shows total time or number of stops depending on the algorithm used.
   - display_network_info(): shows a summary of the selected city: lines, total stations, transfer hubs, and whether the network is fully connected.


# 4 ui/menu.py — User Input

Purpose: Handles everything the user types in the terminal.

   - ask_station(): lets you type a station name with fuzzy matching, so a partial or slightly wrong name will still find the right station.
   - ask_algorithm(): lets you pick between Dijkstra, BFS, and DFS.
   - ask_city(): shows the list of available cities with their line and station counts and lets you pick one.


# 5 main.py — Entry Point

Purpose: Ties everything together. Loads the city data, runs the city picker loop, and launches route planning.

   - Loads all built-in city JSON files from the data/ folder on startup.
   - Accepts extra city files via json flags on the command line.
   - Two nested loops: the outer one handles city selection, the inner one handles route planning and network info within a chosen city.



## **🧪 Testing & Validation**

How can a user verify the code works?


Run python main.py and try the following:

   1- Pick a city --> check that the station count and lines shown match what you'd expect.
   2- Plan a route with Dijkstra --> verify the estimated time looks reasonable and transfers are shown correctly.
   3- Plan the same route with BFS --> it should show fewer stops but not necessarily the fastest time.
   4- Type a partial station name --> the fuzzy search should suggest the right station.
   5- Load a custom JSON --> run python main.py --json your_file.json and check it appears in the city list.
   6- Network info --> use the i option in the city menu and verify the transfer hubs listed are real interchange stations.


## **📦 Dependencies**

List the main third-party libraries used and _why_ they were chosen:

   - heapq: used in Dijkstra to always process the cheapest node next
   - collections.deque: used in BFS for efficient queue operations
   - collections.defaultdict: used in the graph to build the adjacency list cleanly
   - json: to load city network data from JSON files
   - os / sys: for file paths, terminal clearing, and clean exits


## **🔮 Future Roadmap (v2.0)**

What features would you add if you had more time or a larger budget?

   - Graphical map view showing the route drawn on an actual metro map
   - Accessibility options --> avoid stairs, prefer lifts at transfer stations
   - Real-time disruption alerts--> mark a line as closed and reroute automatically
