from src.domain.models.v_common import UUID, DateTime
from src.domain.models.base_model import Entity

class Period(Entity):
    """ 
    Represents usually a legislative period, with a label and description. 
    Can reference other legislative cycles.
    """
    def __init__(
        self,
        id: UUID,
        label: str,
        start_date: DateTime,
        end_date: DateTime,
        description: str,
    ):
        self.id = id
        self.label = label
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Period)
            and self.id == other.id
            and self.label == other.label
            and self.start_date == other.start_date
            and self.end_date == other.end_date
            and self.description == other.description
        )

    def __repr__(self) -> str:
        return f"<Period {self.label} {self.start_date.date()}–{self.end_date.date()}>"
