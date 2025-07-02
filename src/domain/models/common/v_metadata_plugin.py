from typing import Any, Optional
from src.domain.models.common.base_model import ValueObject

class MetadataPlugin(ValueObject):
    """
    Value object for dynamic metadata fields, with loose basic validation (e.g., length).
    Accepts any dictionary of parameters specific to the source/processing.
    """
    def __init__(self, data: Optional[dict[str, Any]] = None):
        self._data = data if data is not None else {}

