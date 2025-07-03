from typing import Optional, Set
from src.domain.models.text.a_speech import Speech
from src.domain.models.base_model import AggregateRoot
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import InstitutionTypeEnum, PartyEnumRegistry, CountryEnum
from src.domain.models.context.v_label import Label
from src.domain.models.context.v_period import Period

#TODO: needs a batch loading or smth like that. Can not process all speeches at once

class Corpora(AggregateRoot):
    def __init__(
        self,
        id: UUID,
        label: Label,
        speeches: Set[Speech],
        country: CountryEnum,
        institution: InstitutionTypeEnum,
        periods: Optional[list[Period]] = None,
        party: Optional[PartyEnumRegistry] = None,
    ):
        super().__init__(id)
        self._label = label
        self._speeches = speeches
        self._institution = institution
        self._party = party
        self._country = country
        self._periods = periods

    @property
    def label(self) -> Label:
        return self._label

    @label.setter
    def label(self, value: Label):
        self._label = value

    @property
    def speeches(self) -> Set[Speech]:
        return self._speeches

    @speeches.setter
    def speeches(self, value: Set[Speech]):
        self._speeches = value

    @property
    def institution(self) -> Optional[InstitutionTypeEnum]:
        return self._institution

    @property
    def party(self) -> Optional[PartyEnumRegistry]:
        return self._party

    @property
    def country(self) -> Optional[CountryEnum]:
        return self._country

    @property
    def periods(self) -> Optional[list[Period]]:
        return self._periods

    def __len__(self) -> int:
        return len(self._speeches)
