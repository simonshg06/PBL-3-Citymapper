from core.graph import TransitGraph


def prompt(text: str) -> str: # Simple wrapper around input() to standardize prompts and strip whitespace
    return input(text).strip()

def ask_station(label: str, graph: TransitGraph) -> str: 
    # this function prompts the user to enter a station name, and attempts to match it to the graph's stations    
    stations = graph.all_stations()
    while True:
        raw = prompt(f"  {label}: ").strip()

        if raw in graph.station_lines:
            return raw

        # Fuzzy: case-insensitive substring search
        matches = [s for s in stations if raw.lower() in s.lower()]

        if len(matches) == 1:
            confirm = prompt(f"  Did you mean '{matches[0]}'? [Y/n] ").lower()
            if confirm in ("", "y", "yes"):
                return matches[0]

        elif matches:
            print(f"  Multiple matches for '{raw}':")
            for i, m in enumerate(matches[:10], 1):
                print(f"    {i}. {m}")
            choice = prompt(f"  Enter number (1-{min(10, len(matches))}) or 0 to retype: ")
            if choice.isdigit() and 1 <= int(choice) <= min(10, len(matches)):
                return matches[int(choice) - 1]

        else:
            print(f"  ✘  Station not found: '{raw}'. Try again.")


# Maps number input to algorithm name
def ask_algorithm():

    print("\n  Algorithms:")
    print("    1. Dijkstra  — fastest route (shortest time)")
    print("    2. BFS       — fewest stops")
    print("    3. DFS       — depth-first exploration")

    options = {"1": "dijkstra", "2": "bfs", "3": "dfs"}

    while True:

        choice = prompt("  Choose [1/2/3, default=1]: ") or "1"  # treat empty input as "1"

        if choice in options: return options[choice]
        print("  Please enter 1, 2 or 3.")

# Shows city list and returns the chosen city name, or None if user quits
def ask_city(city_names, networks):
    print("\n  Available cities:")
    for i, name in enumerate(city_names, 1):
        data = networks[name]
        num_stations = len({st for l in data["lignes"].values() for st in l["stations"]})  # count unique stations across all lines
        print(f"    {i}. {name:<20} ({len(data['lignes'])} lines, {num_stations} stations)")
    print(f"    {len(city_names) + 1}. Quit")

    raw = prompt("\n  Select a city: ")
    if raw.isdigit():
        idx = int(raw)
        if idx == len(city_names) + 1: return None          # user picked Quit
        if 1 <= idx <= len(city_names): return city_names[idx - 1]  # valid city number
    return raw if raw in networks else ""  # typed a city name, or garbage input