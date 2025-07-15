from typing import Optional
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_common import DateTime
from src.domain.models.common.v_enums import OwnerTypeEnum
from src.domain.models.base_entity import Entity
from src.domain.models.context.v_label import Label

class Period(Entity):
    """Justified time between two dates"""
    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        owner_type: OwnerTypeEnum,
        label: Label,
        start_date: DateTime,
        end_date: DateTime,
        description: Optional[str] = None,
    ):
        super().__init__(id)
        self._owner_id = owner_id
        self._owner_type = owner_type
        self._label = label
        self._start_date = start_date
        self._end_date = end_date
        if start_date.value > end_date.value:
            raise ValueError("Start date must be before end date")
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

    @property
    def owner_type(self) -> OwnerTypeEnum:
        return self._owner_type

    # TODO: Needs just a little of constraint
    @description.setter
    def description(self, value: Optional[str]):
        self._description = value

    def to_range_dict(self) -> Optional[dict[str, DateTime]]:
        """Convert the Period to a dictionary with start and end dates."""
        if not self.start_date or not self.end_date:
            return None
        return {
            "start_date": self.start_date,
            "end_date": self.end_date
        }
    
    def __repr__(self) -> str:
        label = self._label
        start = self._start_date.value
        end = self._end_date.value
        return f"<Period {label} {start}–{end}>"