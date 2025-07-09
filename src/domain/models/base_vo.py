from abc import ABC
from dataclasses import dataclass

@dataclass    
class ValueObject(ABC):
    """Base class for value objects."""
    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and vars(self) == vars(other)
    
    def __hash__(self) -> int:
        return hash(tuple(sorted(vars(self).items())))
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"
    
