from dataclasses import dataclass


@dataclass
class ResponseProtocol:
    """Internal Parsed response with all required fields."""

    date: str
    title: str
    source: str
    text: str
