from typing import Optional

from src.domain.irepository.text.i_text_ngrams import INGramizedTextRepository
from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_ngrams import NGramizedText
from src.infrastructure.mappers.text.m_text_ngrams import NGramizedTextMapper
from src.infrastructure.orm.orm_session import session_scope
from src.infrastructure.orm.text.orm_text_ngrams import TextNgramsORM


class NGramizedTextRepository(INGramizedTextRepository):
    def get_by_id(self, id: UUID) -> Optional[NGramizedText]:
        with session_scope() as session:
            orm_ngram = (
                session.query(TextNgramsORM)
                .filter_by(id=id.value)
                .one_or_none()
            )
            if orm_ngram:
                return NGramizedTextMapper.to_domain(orm_ngram)
            return None

    def get_by_speech_id(self, speech_id: UUID) -> Optional[NGramizedText]:
        with session_scope() as session:
            orm_ngram = (
                session.query(TextNgramsORM)
                .filter_by(speech_text_id=speech_id.value)
                .one_or_none()
            )
            if orm_ngram:
                return NGramizedTextMapper.to_domain(orm_ngram)
            return None

    def add(self, ngramized_text: NGramizedText) -> None:
        with session_scope() as session:
            orm_ngram = NGramizedTextMapper.to_orm(ngramized_text)
            session.add(orm_ngram)

    def update(self, ngramized_text: NGramizedText) -> None:
        with session_scope() as session:
            exists = (
                session.query(TextNgramsORM)
                .filter_by(id=ngramized_text.id.value)
                .one_or_none()
            )
            if not exists:
                raise ValueError(
                    f"NGramizedText with id {ngramized_text.id} not found."
                )
            orm_ngram = NGramizedTextMapper.to_orm(ngramized_text)
            session.merge(orm_ngram)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_ngram = (
                session.query(TextNgramsORM)
                .filter_by(id=id.value)
                .one_or_none()
            )
            if orm_ngram:
                session.delete(orm_ngram)
