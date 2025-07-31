from backend.domain.models.base_vo import ValueObject


class Agenda(ValueObject):
    """Represents an agenda for protocol texts"""

    def __init__(self, items: dict[str, list[str]]):
        self._items = items

    @property
    def items(self) -> dict[str, list[str]]:
        return self._items

    def all_types(self) -> list[str]:
        return list(self._items.keys())
