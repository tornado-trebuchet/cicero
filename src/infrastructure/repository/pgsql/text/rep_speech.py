from typing import List, Optional

from src.domain.irepository.text.i_speech import ISpeechRepository
from src.domain.models.common.v_common import UUID, DateTime
from src.domain.models.context.e_period import Period
from src.domain.models.text.a_speech import Speech
from src.infrastructure.mappers.text.m_speech import SpeechMapper
from src.infrastructure.orm.orm_session import session_scope
from src.infrastructure.orm.text.orm_speech import SpeechORM
from src.infrastructure.orm.text.orm_protocol import ProtocolORM
from src.infrastructure.orm.context.orm_institution import InstitutionORM
from src.infrastructure.orm.context.orm_speaker import SpeakerORM


class SpeechRepository(ISpeechRepository):
    def get_by_id(self, id: UUID) -> Optional[Speech]:
        with session_scope() as session:
            orm_speech = (
                session.query(SpeechORM).filter_by(id=id.value).one_or_none()
            )
            return SpeechMapper.to_domain(orm_speech) if orm_speech else None

    def get_by_id_list(self, id_list: List[UUID]) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .filter(SpeechORM.id.in_([id.value for id in id_list]))
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_country_id(self, country_id: UUID) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.protocol)
                .join(ProtocolORM.institution)
                .filter_by(country_id=country_id.value)
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_country_id_list(self, country_id_list: List[UUID]) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.protocol)
                .join(ProtocolORM.institution)
                .filter(InstitutionORM.country_id.in_([cid.value for cid in country_id_list]))
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_institution_id(self, institution_id: UUID) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.protocol)
                .filter_by(institution_id=institution_id.value)
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_institution_id_list(self, institution_id_list: List[UUID]) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.protocol)
                .filter(ProtocolORM.institution_id.in_([iid.value for iid in institution_id_list]))
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_protocol_id(self, protocol_id: UUID) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .filter_by(protocol_id=protocol_id.value)
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_protocol_id_list(self, protocol_id_list: List[UUID]) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .filter(SpeechORM.protocol_id.in_([pid.value for pid in protocol_id_list]))
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_party_id(self, party_id: UUID) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.speaker)
                .filter_by(party_id=party_id.value)
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_party_id_list(self, party_id_list: List[UUID]) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.speaker)
                .filter(SpeakerORM.party_id.in_([pid.value for pid in party_id_list]))
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_speaker_id(self, speaker_id: UUID) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .filter_by(speaker_id=speaker_id.value)
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def get_by_speaker_id_list(self, speaker_id: List[UUID]) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .filter(SpeechORM.speaker_id.in_([sid.value for sid in speaker_id]))
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    # Complex query
    def get_by_date_range(
        self, start_date: DateTime, end_date: DateTime
    ) -> List[Speech]:

        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.protocol)
                .filter(
                    ProtocolORM.date >= start_date,
                    ProtocolORM.date <= end_date,
                )
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    # Complex query
    def get_by_period(self, period: Period) -> List[Speech]:

        with session_scope() as session:
            orm_speeches = (
                session.query(SpeechORM)
                .join(SpeechORM.protocol)
                .filter(
                    ProtocolORM.date >= period.start_date.value,
                    ProtocolORM.date <= period.end_date.value,
                )
                .all()
            )
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    # Use with caution
    def list(self) -> List[Speech]:
        with session_scope() as session:
            orm_speeches = session.query(SpeechORM).all()
            return [SpeechMapper.to_domain(orm) for orm in orm_speeches]

    def add(self, speech: Speech) -> None:
        with session_scope() as session:
            orm_speech = SpeechMapper.to_orm(speech)
            session.add(orm_speech)

    def update(self, speech: Speech) -> None:
        with session_scope() as session:
            exists = (
                session.query(SpeechORM)
                .filter_by(id=speech.id.value)
                .one_or_none()
            )
            if not exists:
                raise ValueError(f"Speech with id {speech.id} not found.")
            orm_speech = SpeechMapper.to_orm(speech)
            session.merge(orm_speech)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_speech = (
                session.query(SpeechORM).filter_by(id=id.value).one_or_none()
            )
            if orm_speech:
                session.delete(orm_speech)