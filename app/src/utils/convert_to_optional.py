from typing import Optional


def convert_to_optional(schema) -> dict:
    """Return a dict with Optional values."""
    return {
        key: Optional[value] for key, value in schema.__annotations__.items()
    }
