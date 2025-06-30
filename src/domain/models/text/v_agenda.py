class Agenda:
    """
    Represents an agenda for a protocol.
    """
    def __init__(self, items: dict[str,list[str]]):
        self._items = items

    @property
    def items(self) -> dict[str, list[str]]:
        """
        Returns the items in the agenda.
        """
        return self._items
    
    def all_types(self) -> list[str]:
        """
        Returns a list of all types in the agenda.
        """
        return list(self._items.keys())

    def __repr__(self):
        return f"Agenda(items={self._items})"

    def __eq__(self, other):
        if not isinstance(other, Agenda):
            return False
        return self._items == other._items

    def __hash__(self):
        return hash(tuple(self._items)) 