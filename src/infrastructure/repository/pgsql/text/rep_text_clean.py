from src.domain.irepository.text.i_text_clean import ICleanTextRepository
from src.domain.models.text.e_text_clean import CleanText
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_text_clean import CleanTextORM
from src.infrastructure.mappers.text.m_text_clean import CleanTextMapper
from infrastructure.orm.orm_session import session_scope
from typing import Optional

class CleanTextRepository(ICleanTextRepository):
    def get_by_id(self, id: UUID) -> Optional[CleanText]:
        with session_scope() as session:
            orm_clean = session.query(CleanTextORM).filter_by(id=id.value).one_or_none()
            if orm_clean:
                return CleanTextMapper.to_domain(orm_clean)
            return None

    def get_by_speech_id(self, speech_id: UUID) -> Optional[CleanText]:
        with session_scope() as session:
            orm_clean = session.query(CleanTextORM).filter_by(speech_text_id=speech_id.value).one_or_none()
            if orm_clean:
                return CleanTextMapper.to_domain(orm_clean)
            return None

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

