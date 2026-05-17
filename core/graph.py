from collections import defaultdict, deque

class TransitGraph:# This class represents the entire transit network as a graph, It stores every station, every line, and every connection between them.
    def __init__(self, network_data):
        self.name = network_data.get("nom", "Unknown")
        self.lignes = network_data.get("lignes", {})  # Store the lines dictionary (e.g. {"1": {"nom": "Ligne 1", "stations":
        self.avg_time = network_data.get("temps_moyen", 120)# Store the average travel time between two consecutive stations in seconds.Used when no explicit connection times are provided in the JSON.

        self.adj = defaultdict(list) # The adjacency list — the core of the graph.Maps each node ("Station::Line") to a list of its neighbours.Each neighbour is stored as: (neighbour_node, travel_time, edge_type, line) defaultdict(list) means: if a key doesn't exist yet, automatically create an empty list for it.
        self.station_lines = defaultdict(set)# Maps each station name to the set of lines that serve it.
        for line_id, line_data in self.lignes.items():
            # line_id is the line name e.g. "1", "A", "T2"
            # line_data is the dictionary for that line e.g. {"nom": ..., "couleur": ..., "stations": [.

            # Go through every station on this line and record that this line serves it.
            for station in line_data["stations"]:
                self.station_lines[station].add(line_id)
            # After this loop, station_lines knows which lines stop at each station.

        # Now build the actual edges of the graph (the connections between nodes).
        self._build_travel_edges(network_data)    # connections along each line
        self._build_transfer_edges(network_data)  # connections between lines at the same station


    def _node(self, station, line):
        # Creates a node name by combining a station and a line with "::" as a separator.
        return f"{station}::{line}"


    def _add_edge(self, from_node, to_node, weight, kind, line):
        # Adds a one-way connection (edge) from from_node to to_node.
        # Stores it as a tuple: (destination, travel_time, edge_type, line)
        # This is what gets stored in the adjacency list (self.adj).
        self.adj[from_node].append((to_node, weight, kind, line))


    def _build_travel_edges(self, data):
        # Builds the edges that represent riding a train/tram between consecutive stations.

        # Check if the JSON has explicit connections listed under "connexions".
        # The "if c" filters out any empty/null entries in the list.
        explicit_connections = [c for c in data.get("connexions", []) if c]

        if explicit_connections:
            for connection in explicit_connections:
                # Build the node names for the two ends of this connection.
                from_node = self._node(connection["de"],   connection["ligne"])
                to_node   = self._node(connection["vers"], connection["ligne"])

                # Add a one-way edge from → to with the given travel time.
                self._add_edge(from_node, to_node, connection["temps"], "travel", connection["ligne"])

        else:
            for line_id, line_data in self.lignes.items():
                stations = line_data["stations"]
                # Go through each consecutive pair of stations on this line.
                for i in range(len(stations) - 1):
                    node_a = self._node(stations[i],     line_id)  # current station
                    node_b = self._node(stations[i + 1], line_id)  # next station

                    # Add edges in BOTH directions (you can travel either way along the line).
                    self._add_edge(node_a, node_b, self.avg_time, "travel", line_id)  # forward
                    self._add_edge(node_b, node_a, self.avg_time, "travel", line_id)  # backward


    def _build_transfer_edges(self, data): # Builds the edges that represent walking between lines at the same station.These are the "correspondances" in the JSON.
        for transfer_point in data.get("correspondances", []):
            station = transfer_point["station"]  # the station where you can transfer
            lines   = transfer_point["lignes"]   # the list of lines that meet here
            time    = transfer_point["temps"]    # how long the transfer takes in seconds
        # Create a transfer edge between every pair of lines at this station
            for line_a in lines:
                for line_b in lines:
                    # Don't create an edge from a line to itself.
                    if line_a != line_b:
                        self._add_edge(
                            self._node(station, line_a),  # you're on line_a at this station
                            self._node(station, line_b),  # you walk to line_b at this station
                            time,
                            "transfer",
                            line_b
                        )

    def all_stations(self):
        # Returns a sorted list of every unique station name in the network.
        # .keys() gives all the station names from station_lines.
        # sorted() puts them in alphabetical order.
        return sorted(self.station_lines.keys())


    def start_nodes(self, station):
        # Given a station name, returns all its nodes (one per line that serves it).
        # Example: start_nodes("Châtelet") → ["Châtelet::1", "Châtelet::4", "Châtelet::7", ...]
        # The algorithms use this to start from ALL possible lines at the departure station.
        return [self._node(station, line) for line in self.station_lines[station]]


    def end_nodes(self, station):
        # Same as start_nodes but returns a SET instead of a list.
        # A set is used because checking "is this node in the destination?" is faster with a set.
        # Example: end_nodes("Nation") → {"Nation::1", "Nation::2", "Nation::6", "Nation::9"}
        return {self._node(station, line) for line in self.station_lines[station]}


    def transfer_stations(self):
        # Returns a list of all stations served by more than one line.
        return [station for station, lines in self.station_lines.items() if len(lines) > 1]


    def is_connected(self):
        # Checks whether the entire graph is connected —
        if not self.adj:
            return True
        # Pick any one node to start from.
        # next(iter(...)) just grabs the first key from the dictionary.
        start_node = next(iter(self.adj))

        # visited tracks every node we've successfully reached.
        visited = {start_node}

        # queue holds nodes we need to explore next (same BFS logic as the BFS algorithm).
        queue = deque([start_node])

        while queue:
            current_node = queue.popleft()
            # The "*, _" syntax means "take the first item (the neighbour),
            # and ignore everything else (weight, type, line)".
            for neighbour, *_ in self.adj[current_node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        # Build the set of ALL nodes that exist in the graph —
        # both nodes that have outgoing edges (keys in self.adj)
        # and nodes that only appear as destinations (values in self.adj).
        all_nodes = set(self.adj) | {neighbour for edges in self.adj.values() for neighbour, *_ in edges}
        # The | operator merges two sets together.

        # If every node was visited, the graph is fully connected.
        return visited == all_nodes