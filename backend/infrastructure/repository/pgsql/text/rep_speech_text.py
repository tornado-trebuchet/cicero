from typing import Optional

from backend.domain.irepository.text.i_speech_text import ISpeechTextRepository
from backend.domain.models.common.v_common import UUID
from backend.domain.models.text.a_speech_text import SpeechText
from backend.infrastructure.mappers.text.m_speech_text import SpeechTextMapper
from backend.infrastructure.orm.orm_session import session_scope
from backend.infrastructure.orm.text.orm_speech_text import SpeechTextORM


class SpeechTextRepository(ISpeechTextRepository):
    def get_by_id(self, id: UUID) -> Optional[SpeechText]:
        with session_scope() as session:
            orm_speech_text = session.query(SpeechTextORM).filter_by(id=id.value).one_or_none()
            if orm_speech_text:
                return SpeechTextMapper.to_domain(orm_speech_text)
            return None

    def add(self, speech_text: SpeechText) -> None:
        with session_scope() as session:
            orm_speech_text = SpeechTextMapper.to_orm(speech_text)
            session.add(orm_speech_text)

    def update(self, speech_text: SpeechText) -> None:
        with session_scope() as session:
            exists = session.query(SpeechTextORM).filter_by(id=speech_text.id.value).one_or_none()
            if not exists:
                raise ValueError(f"SpeechText with id {speech_text.id} not found.")
            orm_speech_text = SpeechTextMapper.to_orm(speech_text)
            session.merge(orm_speech_text)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_speech_text = session.query(SpeechTextORM).filter_by(id=id.value).one_or_none()
            if orm_speech_text:
                session.delete(orm_speech_text)
