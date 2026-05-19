from core.graph import TransitGraph


def prompt(text: str) -> str: # Simple wrapper around input() to standardize prompts and strip whitespace
    return input(text).strip() # user inputs a string, and we remove any leading or trailing whitespace for cleaner processing

def ask_station(label: str, graph: TransitGraph) -> str:
    # this function prompts the user to enter a station name, and attempts to match it to the graph's stations    
    stations = graph.all_stations() # gets the list of full station names from the graph
    while True:
        raw = prompt(f"  {label}: ").strip() # prompts the user with the given label (e.g. "Departure station") and gets their input, stripping whitespace
        if raw in graph.station_lines: # if the raw input matches a station name in the graph, we return it immediately
            return raw

        # Fuzzy: case-insensitive substring search
        matches = [s for s in stations if raw.lower() in s.lower()] 
        # finds all stations that contain the user's input as a substring, ignoring case. This allows for partial matches and is more forgiving of typos or incomplete names.

        if len(matches) == 1:
             # if there's exactly one match, we can be confident that's what the user meant, so we ask for confirmation
            confirm = prompt(f"  Did you mean '{matches[0]}'? [Y/n] ").lower()
             # asks the user to confirm if the single match is correct, treating "y" or empty input as confirmation
            if confirm in ("", "y", "yes"):
                # if confirmed, we return the matched station name
                return matches[0]

        elif matches: # if there are multiple matches, we list them and ask the user to choose by number
            print(f"  Multiple matches for '{raw}':") # if the user's input is ambiguous and matches multiple stations, we inform them and show the options
            for i, m in enumerate(matches[:10], 1): # we show up to the first 10 matches with a number for selection
                print(f"    {i}. {m}") # prints each match with an index number for the user to choose from
            choice = prompt(f"  Enter number (1-{min(10, len(matches))}) or 0 to retype: ") # prompts the user to enter the number corresponding to their intended station, or 0 to go back and type again
            if choice.isdigit() and 1 <= int(choice) <= min(10, len(matches)): # if the user enters a valid number corresponding to one of the matches, we return that station
                return matches[int(choice) - 1] # returns the station name corresponding to the user's numeric choice (adjusting for 0-based index)

        else:
            print(f"  ✘  Station not found: '{raw}'. Try again.") # if no matches are found, we inform the user and prompt them to try again


# Maps number input to algorithm name
def ask_algorithm():

    print("\n  Algorithms:")
    print("    1. fastest route (shortest time)")
    print("    2. fewest stops")
    print("    3. depth-first exploration")

    options = {"1": "Fatest route", "2": "Fewest stops", "3": "depth first exploration"}

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