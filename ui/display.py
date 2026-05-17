from core.algorithms import parse_node
from core.graph import TransitGraph

SEP  = "─" * 60


def format_time(seconds: int) -> str: # Format a time duration given in seconds into a human-readable string
    m, s = divmod(seconds, 60)
    if m == 0:
        return f"{s}s"
    return f"{m} min {s}s" if s else f"{m} min"