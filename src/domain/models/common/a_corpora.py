from typing import Optional, Set, List
from src.domain.models.base_model import AggregateRoot
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label
from src.domain.models.context.v_period import Period

class Corpora(AggregateRoot):
    def __init__(
        self,
        id: UUID,
        label: Label,
        speeches: Set[UUID],
        countries: Optional[List[UUID]] = None,
        institutions: Optional[List[UUID]] = None,
        periods: Optional[List[UUID]] = None,
        parties: Optional[List[UUID]] = None,
        speakers: Optional[List[UUID]] = None,
    ):
        super().__init__(id)
        self._label = label
        self._speeches = speeches
        self._countries = countries
        self._institutions = institutions
        self._periods = periods
        self._parties = parties
        self._speakers = speakers

    @property
    def label(self) -> Label:
        return self._label

    @label.setter
    def label(self, value: Label):
        self._label = value

    @property
    def speeches(self) -> Set[UUID]:
        return self._speeches

    @speeches.setter
    def speeches(self, value: Set[UUID]):
        self._speeches = value

    @property
    def countries(self) -> Optional[List[UUID]]:
        return self._countries

    @property
    def institutions(self) -> Optional[List[UUID]]:
        return self._institutions

    @property
    def periods(self) -> Optional[List[Period]]:
        return self._periods

    @property
    def parties(self) -> Optional[List[PartyEnum]]:
        return self._parties

    @property
    def speakers(self) -> Optional[List[UUID]]:
        return self._speakers

    def __len__(self) -> int:
        return len(self._speeches)
