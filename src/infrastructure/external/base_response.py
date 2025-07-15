from dataclasses import dataclass
from typing import Any, Optional, Dict

@dataclass
class ResponseProtocol:
    """Internal Parsed response with all required fields."""
    date: str
    title: str
    link: Optional[str]
    agenda: Optional[Dict[str, Any]]
    text: str