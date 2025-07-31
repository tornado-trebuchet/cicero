from abc import ABC, abstractmethod
from typing import List, Optional

from backend.domain.models.common.v_common import UUID, DateTime
from backend.domain.models.context.e_period import Period
from backend.domain.models.text.a_speech import Speech


class ISpeechRepository(ABC):
    """Speech links text and author"""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Speech]:
        pass

    @abstractmethod
    def get_by_id_list(self, id_list: List[UUID]) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_country_id(self, country_id: UUID) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_country_id_list(self, country_id_list: List[UUID]) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_institution_id(self, institution_id: UUID) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_institution_id_list(self, institution_id_list: List[UUID]) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_protocol_id(self, protocol_id: UUID) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_protocol_id_list(self, protocol_id_list: List[UUID]) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_party_id(self, party_id: UUID) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_party_id_list(self, party_id_list: List[UUID]) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_speaker_id(self, speaker_id: UUID) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_speaker_id_list(self, speaker_id: List[UUID]) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_date_range(self, start_date: DateTime, end_date: DateTime) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_period(self, period: Period) -> List[Speech]:
        pass

    @abstractmethod
    def list(self) -> List[Speech]:
        pass

    @abstractmethod
    def add(self, speech: Speech) -> None:
        pass

    @abstractmethod
    def update(self, speech: Speech) -> None:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass
