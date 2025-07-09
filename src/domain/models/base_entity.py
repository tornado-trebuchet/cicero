from abc import ABC
from src.domain.models.common.v_common import UUID

class Entity(ABC):
    """Base class for entities."""
    def __init__(self, id: UUID):
        self._id = id

    @property
    def id(self) -> UUID:
        return self._id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._id}>"