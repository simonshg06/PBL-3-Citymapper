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