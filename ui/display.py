from core.algorithms import parse_node
from core.graph import TransitGraph

SEP  = "─" * 60


def format_time(seconds: int) -> str: # Format a time duration given in seconds into a human-readable string
    m, s = divmod(seconds, 60)
    if m == 0:
        return f"{s}s"
    return f"{m} min {s}s" if s else f"{m} min"




def display_route(path: list, total_cost, graph: TransitGraph, algorithm_name: str): # Print a nicely formatted travel route
    """Print a nicely formatted itinerary."""
    print()
    print(SEP)
    print(f"  Route found by {algorithm_name}")
    print(SEP)

    if not path:
        print("  (empty path)")
        return

    transfers = 0

    for i, (node, info) in enumerate(path):
        station, line = parse_node(node)
        kind = info.get("type", "start")

        if i == 0:
            print(f"\n  🚉 Board at  : {station}  [Line {line}]")
        elif kind == "transfer":
            print(f"  🔄 Transfer  : {station}  — change to Line {line}")
            transfers += 1
        elif i == len(path) - 1:
            print(f"  🏁 Alight at : {station}  [Line {line}]")
        else:
            print(f"     →  {station}")

    print()
    print(SEP)
    if total_cost is not None:
        print(f"  ⏱  Estimated time : {format_time(total_cost)}")
    else:
        print(f"  🛑 Stops : {len(path) - 1}")
    print(f"  🔄 Transfers     : {transfers}")
    print(SEP)
    print()


def display_network_info(graph: TransitGraph):
    transfers = graph.transfer_stations()
    preview   = ", ".join(transfers[:6]) + (" …" if len(transfers) > 6 else "")
    connected = "Yes ✔" if graph.is_connected() else "No — isolated nodes detected ✘"

    print(f"\n{SEP}")
    print(f"  Network : {graph.name}")
    print(f"  Lines   : {', '.join(graph.lignes.keys())}")
    print(f"  Stations: {len(graph.all_stations())}")
    print(f"  Transfer hubs ({len(transfers)}): {preview}")
    print(f"  Connected: {connected}")
    print(SEP)