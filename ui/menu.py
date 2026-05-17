from core.graph import TransitGraph


def prompt(text: str) -> str: # Simple wrapper around input() to standardize prompts and strip whitespace
    return input(text).strip()