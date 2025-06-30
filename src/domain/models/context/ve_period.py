from typing import Optional
from src.domain.models.common.v_common import UUID, DateTime
from src.domain.models.common.base_model import Entity

class Period(Entity):
    """ 
    Represents usually a legislative period, with a label and description. 
    Can reference other legislative cycles.
    """
    def __init__(
        self,
        id: UUID,
        start_date: DateTime,
        end_date: DateTime,
        label: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(id)
        self._label = label
        self._start_date = start_date
        self._end_date = end_date
        self._description = description

    @property
    def label(self) -> Optional[str]:
        return self._label

    @label.setter
    def label(self, value: Optional[str]):
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

    @description.setter
    def description(self, value: Optional[str]):
        self._description = value

    def __repr__(self) -> str:
        label = self._label if self._label is not None else ""
        start = self._start_date.value if self._start_date is not None else ""
        end = self._end_date.value if self._end_date is not None else ""
        return f"<Period {label} {start}–{end}>"