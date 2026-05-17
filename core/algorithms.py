import heapq # automatically organises a list such that the smallest element is always at the start 
from .graph import TransitGraph # imports TransitGraph class form graph.py


# ── shared helpers ────────────────────────────────────────────

def parse_node(key):# every node is a sation name as the name then the line they are on, the node is split up into tzo strings, the stations name and its line 
    split_position = key.rfind("::") # two colons seperate the name of the stations with its line in order to not confuse the code when a sttion has a colon in its name , the rfind means going from left to right and tells us the position of the ::
    station_name = key[:split_position]       # everything before the "::"
    line_id      = key[split_position + 2:]   # everything after the "::" (skip 2 characters for "::")
 
    return station_name, line_id


def _reconstruct(prev, end_node):#when we arrive at a stop we know how we got there, however it is in reverse order, each station points at where it came from
    path = []
    current = end_node #starts the tracing back from the final destination

    while current is not None:
        # Look up how we got to this station.
        # If somehow it's not in prev, use an empty dictionary as a fallback.
        info = prev.get(current, {})
        path.append((current, info)) # the destiantion goes to the staion it came from and will append the info of that station to the dict 
        current = info.get("from")#we continue moving back until we get to the start station once we get the info.get('from") will return None, stoping the while loop 
    path.reverse() # the path is written as destination first then start, this will reverse it 
 
    return path


# ── algorithms ────────────────────────────────────────────────

def dijkstra(graph, departure, arrival):
    possible_destinations = graph.end_nodes(arrival)#this contains all the possible arrival stations, from the data folder
    dist = {}# here will contain the fastest known travel time to reach the destiantion node (cheapest)
    prev = {} # here we will store how we got to each node, we use it at the end to build back up to start 
    priority_queue = [] # this list will be as (cost,node), and as we use heapq, we will always be given the lowest cost first 
 
    for starting_node in graph.start_nodes(departure):
        dist[starting_node] = 0                    
        prev[starting_node] = {"from": None}       # the start has no previous station
        heapq.heappush(priority_queue, (0, starting_node))  # add to the queue with cost 0

    while priority_queue:#this continues as long as there are no more stations left to check 
        cost, current_node = heapq.heappop(priority_queue) # this will pop the station with the lowest trvel time so far 
        if cost > dist.get(current_node, float("inf")):# we use float "inf" to say we havent found any path to the node 
            continue
        if current_node in possible_destinations:
            return _reconstruct(prev, current_node), cost# if we reach the final destination then return the full path with total travel time
        for neighbour, travel_time, edge_type, line in graph.adj[current_node]: # you are at a station and we will now check every neighbour and calculate wether or not a potential transfer is faster or etc
            new_cost = cost + travel_time#new travel time for each neighbour of the station
            if new_cost < dist.get(neighbour, float("inf")):# If this new route is cheaper than what we previously knew, update it.
                dist[neighbour] = new_cost
 
                #the path we took to get to the neighbour 
                prev[neighbour] = {
                    "from":   current_node,
                    "type":   edge_type,
                    "line":   line,
                    "weight": travel_time
                }
 
                heapq.heappush(priority_queue, (new_cost, neighbour))# Add the neighbour to the queue so we explore it later.
    
    return None  # If we exit the loop without finding the destination, no path exists.


def bfs(graph, departure, arrival):
    from collections import deque#we will now use deque as it is a list that is great for adding to the back and removing from the front 
    
    possible_destinations = graph.end_nodes(arrival)
    visited = set()#keeps track of visited staions so we dont go round in circles 
    prev = {} #this once again stores how we reached the station 
    queue = deque()#holds the stations waiting to be analysed
 
    for starting_node in graph.start_nodes(departure):# Initialise the starting stations (one per line at the departure station).
        visited.add(starting_node)              # mark as seen immediately
        prev[starting_node] = {"from": None}   # the start has no previous station
        queue.append(starting_node)             # add to the back of the queue
 
    while queue:# Keep exploring as long as there are stations in the queue.
        current_node = queue.popleft()
 
        if current_node in possible_destinations:# If we've reached the destination, rebuild and return the path.
            path = _reconstruct(prev, current_node)
            number_of_stops = len(path) - 1   # number of edges = nodes minus 1
            return path, number_of_stops
 
        for neighbour, travel_time, edge_type, line in graph.adj[current_node]:# Look at all directly reachable neighbours.
            if neighbour not in visited:
                visited.add(neighbour)   # mark as seen so we don't revisit
                prev[neighbour] = {
                    "from":   current_node,
                    "type":   edge_type,
                    "line":   line,
                    "weight": travel_time
                }
 
                queue.append(neighbour)# Add to the BACK of the queue to explore later.
 
    return None


def dfs(graph, departure, arrival):
    possible_destinations = graph.end_nodes(arrival)
    visited = set()
    prev = {}
    stack = []
 
    for starting_node in graph.start_nodes(departure):
        visited.add(starting_node)
        prev[starting_node] = {"from": None}
        stack.append(starting_node)
 
    while stack:
        current_node = stack.pop() #takes station from top of stack 
        if current_node in possible_destinations:
            path = _reconstruct(prev, current_node)
            number_of_segments = len(path) - 1
            return path, number_of_segments
        for neighbour, travel_time, edge_type, line in graph.adj[current_node]:
            if neighbour not in visited:
                visited.add(neighbour)
 
                prev[neighbour] = {
                    "from":   current_node,
                    "type":   edge_type,
                    "line":   line,
                    "weight": travel_time
                }

                stack.append(neighbour)
 
    return None
 