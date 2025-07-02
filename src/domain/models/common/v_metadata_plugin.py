from typing import Any, Optional
from src.domain.models.base_model import ValueObject

class MetadataPlugin(ValueObject):
    """
    Value object for dynamic metadata fields, with loose basic validation (e.g., length).
    Accepts any dictionary of parameters specific to the source/processing.
    """
    def __init__(
        self, 
        data: Optional[dict[str, Any]] = None
    ):
        self._data = data

    def set_property(self, key: str, value: Any) -> None:
        if self._data is None:
            self._data = {}
        self._data[key] = value
    
    def get_properties(self) -> Optional[dict[str, Any]]:
        return self._data
    
    def get_property(self, key: str) -> Optional[Any]:
        if self._data is not None:
            return self._data.get(key)
        return None
    
    def remove_property(self, key: str) -> None:
        if self._data is not None and key in self._data:
            del self._data[key]
    
    

