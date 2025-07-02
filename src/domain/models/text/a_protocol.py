from typing import Optional
from src.domain.models.common.v_common import UUID, DateTime, HttpUrl
from src.domain.models.common.base_model import AggregateRoot
from src.domain.models.common.v_enums import ProtocolTypeEnum
from src.domain.models.text.v_protocol_text import ProtocolText
from src.domain.models.text.v_protocol_agenda import Agenda
from src.domain.models.context.v_period import Period
from src.domain.models.text.a_speech import Speech

class Protocol(AggregateRoot):
    """Represents a protocol e.g., parliamentary session."""
    def __init__(
        self,
        id: UUID,
        country_id: UUID,
        institution_id: UUID,
        date: DateTime,
        protocol_type: ProtocolTypeEnum,
        protocol_text: ProtocolText,
        protocol_speeches: Optional[list[Speech]] = None,
        agenda: Optional[Agenda] = None,
        period: Optional[Period] = None,
        file_source: Optional[HttpUrl] = None,
        metadata: Optional[dict] = None,
    ):
        super().__init__(id)
        self._country_id = country_id
        self._institution_id = institution_id
        self._period = period if period is not None else None
        self._file_source = file_source
        self._protocol_type = protocol_type
        self._protocol_text = protocol_text
        self._protocol_speeches = protocol_speeches if protocol_speeches is not None else []
        self._agenda = agenda if agenda is not None else None
        self._date = date
        self._metadata = metadata if metadata is not None else {}

    @property
    def country_id(self) -> UUID:
        return self._country_id

    @property
    def institution_id(self) -> UUID:
        return self._institution_id

    @institution_id.setter
    def institution_id(self, value: UUID):
        self._institution_id = value

    @property
    def period(self) -> Optional[Period]:
        return self._period

    @period.setter
    def period(self, value: Optional[Period]):
        self._period = value

    @property
    def file_source(self) -> Optional[HttpUrl]:
        return self._file_source

    @file_source.setter
    def file_source(self, value: Optional[HttpUrl]):
        self._file_source = value

    @property
    def protocol_type(self) -> ProtocolTypeEnum:
        return self._protocol_type

    @protocol_type.setter
    def protocol_type(self, value: ProtocolTypeEnum):
        self._protocol_type = value

    @property
    def date(self) -> DateTime:
        return self._date

    @date.setter
    def date(self, value: DateTime):
        self._date = value

    @property
    def protocol_text(self) -> ProtocolText:
        return self._protocol_text
    
    @protocol_text.setter
    def protocol_text(self, value: ProtocolText):
        self._protocol_text = value

    @property
    def metadata(self) -> dict:
        return self._metadata

    @metadata.setter
    def metadata(self, value: dict):
        self._metadata = value

    def __repr__(self) -> str:
        return f"<Protocol {self._protocol_type} {self._date} {self.id}>"
