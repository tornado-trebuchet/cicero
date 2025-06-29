from typing import Any, Optional

class MetadataPlugin:
    """
    Value object for dynamic metadata fields, with loose basic validation (e.g., length).
    Accepts any dictionary of parameters specific to the source/processing.
    """
    def __init__(self, data: Optional[dict[str, Any]] = None):
        self._data = data if data is not None else {}

    def __eq__(self, other) -> bool:
        return isinstance(other, MetadataPlugin) and self._data == other._data

    def __repr__(self) -> str:
        return f"<MetadataPlugin {self._data}>"
