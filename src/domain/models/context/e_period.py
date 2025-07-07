from typing import Optional
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_common import DateTime
from src.domain.models.base_model import Entity
from src.domain.models.context.v_label import Label

class Period(Entity):
    """Justified time between two dates"""
    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        label: Label,
        start_date: DateTime,
        end_date: DateTime,
        description: Optional[str] = None,
    ):
        super().__init__(id)
        self._label = label
        self._start_date = start_date
        self._end_date = end_date
        if start_date.value > end_date.value:
            raise ValueError("Start date must be before end date")
        self._owner_id = owner_id
        self._description = description

    @property
    def label(self) -> Label:
        return self._label

    @label.setter
    def label(self, value: Label):
        self._label = value

    @property
    def start_date(self) -> DateTime:
        return self._start_date

    @property
    def end_date(self) -> DateTime:
        return self._end_date

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def owner_id(self) -> UUID:
        return self._owner_id

    # TODO: Needs just a little of constraint
    @description.setter
    def description(self, value: Optional[str]):
        self._description = value

    def __repr__(self) -> str:
        label = self._label
        start = self._start_date.value if self._start_date is not None else ""
        end = self._end_date.value if self._end_date is not None else ""
        return f"<Period {label} {start}–{end}>"