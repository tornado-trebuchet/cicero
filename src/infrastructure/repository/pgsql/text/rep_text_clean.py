from typing import Optional, List

from src.domain.irepository.text.i_text_clean import ICleanTextRepository
from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_clean import CleanText
from src.infrastructure.mappers.text.m_text_clean import CleanTextMapper
from src.infrastructure.orm.orm_session import session_scope
from src.infrastructure.orm.text.orm_text_clean import CleanTextORM
from src.infrastructure.orm.text.orm_speech import SpeechORM
from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM


class CleanTextRepository(ICleanTextRepository):
    def get_by_id(self, id: UUID) -> Optional[CleanText]:
        with session_scope() as session:
            orm_clean = session.query(CleanTextORM).filter_by(id=id.value).one_or_none()
            if orm_clean:
                return CleanTextMapper.to_domain(orm_clean)
            return None

    def get_by_speech_id(self, speech_id: UUID) -> Optional[CleanText]:
        with session_scope() as session:
            from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM

            speech_text = session.query(SpeechTextORM).filter_by(speech_id=speech_id.value).one_or_none()
            if not speech_text:
                return None
            orm_clean = session.query(CleanTextORM).filter_by(speech_text_id=speech_text.id).one_or_none()
            if orm_clean:
                return CleanTextMapper.to_domain(orm_clean)
            return None

    def get_by_speech_ids(self, speech_ids: List[UUID]) -> List[str]:
        with session_scope() as session:
            speech_id_values = [sid.value for sid in speech_ids]

            clean_texts = (
                session.query(CleanTextORM.clean_text)
                .join(SpeechTextORM, CleanTextORM.speech_text_id == SpeechTextORM.id)
                .join(SpeechORM, SpeechTextORM.speech_id == SpeechORM.id)
                .filter(SpeechORM.id.in_(speech_id_values))
                .all()
            )

            return [text[0] for text in clean_texts if text[0]]

    def add(self, clean_text: CleanText) -> None:
        with session_scope() as session:
            orm_clean = CleanTextMapper.to_orm(clean_text)
            session.add(orm_clean)

    def update(self, clean_text: CleanText) -> None:
        with session_scope() as session:
            exists = session.query(CleanTextORM).filter_by(id=clean_text.id.value).one_or_none()
            if not exists:
                raise ValueError(f"CleanText with id {clean_text.id} not found.")
            orm_clean = CleanTextMapper.to_orm(clean_text)
            session.merge(orm_clean)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_clean = session.query(CleanTextORM).filter_by(id=id.value).one_or_none()
            if orm_clean:
                session.delete(orm_clean)
