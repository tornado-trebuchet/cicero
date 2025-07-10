from src.domain.irepository.text.i_text_split import ITextSentencesRepository
from src.domain.models.text.e_text_split import TextSentences
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_text_split import SplitTextORM
from src.infrastructure.mappers.text.m_text_split import TextSentencesMapper
from infrastructure.orm.orm_session import session_scope
from typing import Optional

class TextSentencesRepository(ITextSentencesRepository):
    def get_by_id(self, id: UUID) -> Optional[TextSentences]:
        with session_scope() as session:
            orm_split = session.query(SplitTextORM).filter_by(id=id.value).one_or_none()
            if orm_split:
                return TextSentencesMapper.to_domain(orm_split)
            return None

    def get_by_speech_id(self, speech_id: UUID) -> Optional[TextSentences]:
        with session_scope() as session:
            orm_split = session.query(SplitTextORM).filter_by(speech_text_id=speech_id.value).one_or_none()
            if orm_split:
                return TextSentencesMapper.to_domain(orm_split)
            return None

    def add(self, text_sentences: TextSentences) -> None:
        with session_scope() as session:
            orm_split = TextSentencesMapper.to_orm(text_sentences)
            session.add(orm_split)

    def update(self, text_sentences: TextSentences) -> None:
        with session_scope() as session:
            exists = session.query(SplitTextORM).filter_by(id=text_sentences.id.value).one_or_none()
            if not exists:
                raise ValueError(f"TextSentences with id {text_sentences.id} not found.")
            orm_split = TextSentencesMapper.to_orm(text_sentences)
            session.merge(orm_split)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_split = session.query(SplitTextORM).filter_by(id=id.value).one_or_none()
            if orm_split:
                session.delete(orm_split)