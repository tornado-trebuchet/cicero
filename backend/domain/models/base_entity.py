from abc import ABC

from backend.domain.models.common.v_common import UUID


class Entity(ABC):
    __slots__ = ("_id",)

    def __init__(self, id: UUID):
        object.__setattr__(self, "_id", id)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "_id":
            raise AttributeError("Cannot modify Entity id once set")
        super().__setattr__(name, value)

    @property
    def id(self) -> UUID:
        return self._id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._id}>"
