from typing import List, Optional, Set

from src.domain.models.base_aggregate import AggregateRoot
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label


class Corpora(AggregateRoot):
    def __init__(
        self,
        id: UUID,
        label: Label,
        texts: Set[UUID],
        countries: Optional[List[UUID]] = None,
        institutions: Optional[List[UUID]] = None,
        protocols: Optional[List[UUID]] = None,
        parties: Optional[List[UUID]] = None,
        speakers: Optional[List[UUID]] = None,
        periods: Optional[List[UUID]] = None,
    ):
        super().__init__(id)
        self._label = label
        self._texts = texts
        self._countries = countries
        self._institutions = institutions
        self._protocols = protocols
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
    def texts(self) -> Set[UUID]:
        return self._texts

    @texts.setter
    def texts(self, value: Set[UUID]):
        self._texts = value

    @property
    def countries(self) -> Optional[List[UUID]]:
        return self._countries

    @property
    def institutions(self) -> Optional[List[UUID]]:
        return self._institutions

    @property
    def periods(self) -> Optional[List[UUID]]:
        return self._periods

    @property
    def parties(self) -> Optional[List[UUID]]:
        return self._parties

    @property
    def speakers(self) -> Optional[List[UUID]]:
        return self._speakers

    def __len__(self) -> int:
        return len(self._texts)
