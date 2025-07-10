from src.domain.irepository.text.i_text_tokenized import ITokenizedTextRepository
from src.domain.models.text.e_text_tokenized import TokenizedText
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_text_tokenized import TokenizedTextORM
from src.infrastructure.mappers.text.m_text_tokenized import TokenizedTextMapper
from infrastructure.orm.orm_session import session_scope
from typing import Optional

class TokenizedTextRepository(ITokenizedTextRepository):
    def get_by_id(self, id: UUID) -> Optional[TokenizedText]:
        with session_scope() as session:
            orm_tokenized = session.query(TokenizedTextORM).filter_by(id=id.value).one_or_none()
            if orm_tokenized:
                return TokenizedTextMapper.to_domain(orm_tokenized)
            return None

    def get_by_speech_id(self, speech_id: UUID) -> Optional[TokenizedText]:
        with session_scope() as session:
            orm_tokenized = session.query(TokenizedTextORM).filter_by(speech_text_id=speech_id.value).one_or_none()
            if orm_tokenized:
                return TokenizedTextMapper.to_domain(orm_tokenized)
            return None

    def add(self, tokenized_text: TokenizedText) -> None:
        with session_scope() as session:
            orm_tokenized = TokenizedTextMapper.to_orm(tokenized_text)
            session.add(orm_tokenized)

    def update(self, tokenized_text: TokenizedText) -> None:
        with session_scope() as session:
            exists = session.query(TokenizedTextORM).filter_by(id=tokenized_text.id.value).one_or_none()
            if not exists:
                raise ValueError(f"TokenizedText with id {tokenized_text.id} not found.")
            orm_tokenized = TokenizedTextMapper.to_orm(tokenized_text)
            session.merge(orm_tokenized)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_tokenized = session.query(TokenizedTextORM).filter_by(id=id.value).one_or_none()
            if orm_tokenized:
                session.delete(orm_tokenized)