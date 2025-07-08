from src.domain.irepository.text.I_speech_text import ISpeechTextRepository
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM
from src.infrastructure.mappers.text.m_speech_text import SpeechTextMapper
from src.infrastructure.orm.session import session_scope
from typing import Optional

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