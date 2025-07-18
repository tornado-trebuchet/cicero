from src.domain.irepository.text.i_text_translated import ITranslatedTextRepository
from src.domain.models.text.e_text_translated import TranslatedText
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_text_translated import TranslatedTextORM
from src.infrastructure.mappers.text.m_text_translated import TranslatedTextMapper
from src.infrastructure.orm.orm_session import session_scope
from typing import Optional

class TranslatedTextRepository(ITranslatedTextRepository):
    def get_by_id(self, id: UUID) -> Optional[TranslatedText]:
        with session_scope() as session:
            orm_translated = session.query(TranslatedTextORM).filter_by(id=id.value).one_or_none()
            if orm_translated:
                return TranslatedTextMapper.to_domain(orm_translated)
            return None

    def get_by_speech_id(self, speech_id: UUID) -> Optional[TranslatedText]:
        with session_scope() as session:
            orm_translated = session.query(TranslatedTextORM).filter_by(speech_text_id=speech_id.value).one_or_none()
            if orm_translated:
                return TranslatedTextMapper.to_domain(orm_translated)
            return None

    def add(self, translated_text: TranslatedText) -> None:
        with session_scope() as session:
            orm_translated = TranslatedTextMapper.to_orm(translated_text)
            session.add(orm_translated)

    def update(self, translated_text: TranslatedText) -> None:
        with session_scope() as session:
            exists = session.query(TranslatedTextORM).filter_by(id=translated_text.id.value).one_or_none()
            if not exists:
                raise ValueError(f"TranslatedText with id {translated_text.id} not found.")
            orm_translated = TranslatedTextMapper.to_orm(translated_text)
            session.merge(orm_translated)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_translated = session.query(TranslatedTextORM).filter_by(id=id.value).one_or_none()
            if orm_translated:
                session.delete(orm_translated)
