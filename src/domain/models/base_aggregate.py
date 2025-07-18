from src.domain.models.base_entity import Entity
from src.domain.models.common.v_common import UUID


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
        return (
            f"<{self.__class__.__name__} id={self.id}, version={self.version}>"
        )
