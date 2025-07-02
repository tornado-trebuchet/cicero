from abc import ABC
from src.domain.models.common.v_common import UUID
from dataclasses import dataclass

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

@dataclass    
class ValueObject(ABC):
    """Base class for value objects."""
    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and vars(self) == vars(other)
    
    def __hash__(self) -> int:
        return hash(tuple(sorted(vars(self).items())))
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"
    
class AggregateRoot(Entity):
    """Base class for aggregate roots."""
    def __init__(self, id: UUID):
        super().__init__(id)
        self._version = 0

    @property
    def version(self) -> int:
        return self._version

    def increment_version(self):
        self._version += 1

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}, version={self.version}>"