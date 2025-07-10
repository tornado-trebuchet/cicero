from domain.irepository.common.i_corpora import ICorporaRepository
from src.domain.models.common.a_corpora import Corpora
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.common.orm_corpora import CorporaORM
from src.infrastructure.mappers.common.m_corpora import CorporaMapper
from infrastructure.orm.orm_session import session_scope
from typing import Optional, List

class CorporaRepository(ICorporaRepository):
    def get_by_id(self, id: UUID) -> Optional[Corpora]:
        with session_scope() as session:
            orm_corpora = session.query(CorporaORM).filter_by(id=id.value).one_or_none()
            if orm_corpora:
                return CorporaMapper.to_domain(orm_corpora)
            return None

    def list(self) -> List[Corpora]:
        with session_scope() as session:
            orm_corpora = session.query(CorporaORM).all()
            return [CorporaMapper.to_domain(orm) for orm in orm_corpora]

    def add(self, corpora: Corpora) -> None:
        with session_scope() as session:
            orm_corpora = CorporaMapper.to_orm(corpora)
            session.add(orm_corpora)

    def update(self, corpora: Corpora) -> None:
        with session_scope() as session:
            exists = session.query(CorporaORM).filter_by(id=corpora.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Corpora with id {corpora.id} not found.")
            orm_corpora = CorporaMapper.to_orm(corpora)
            session.merge(orm_corpora)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_corpora = session.query(CorporaORM).filter_by(id=id.value).one_or_none()
            if orm_corpora:
                session.delete(orm_corpora)