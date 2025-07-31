from typing import List, Optional

from sqlalchemy.orm import selectinload

from backend.domain.irepository.common.i_corpora import ICorporaRepository
from backend.domain.models.common.a_corpora import Corpora
from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import CountryEnum
from backend.infrastructure.mappers.common.m_corpora import CorporaMapper
from backend.infrastructure.orm.common.orm_corpora import CorporaORM
from backend.infrastructure.orm.text.orm_speech import SpeechORM
from backend.infrastructure.orm.orm_session import session_scope


class CorporaRepository(ICorporaRepository):
    def get_by_id(self, id: UUID) -> Optional[Corpora]:
        with session_scope() as session:
            orm_corpora = (
                session.query(CorporaORM)
                .options(selectinload(CorporaORM.speeches))
                .filter_by(id=id.value)
                .one_or_none()
            )
            if orm_corpora:
                return CorporaMapper.to_domain(orm_corpora)
            return None

    def list(self) -> List[Corpora]:
        with session_scope() as session:
            orm_corpora = (
                session.query(CorporaORM)
                .options(selectinload(CorporaORM.speeches))
                .all()
            )
            return [CorporaMapper.to_domain(orm) for orm in orm_corpora]

    def list_by_country(self, country: CountryEnum) -> List[Corpora]:
        with session_scope() as session:
            orm_corpora = (
                session.query(CorporaORM)
                .options(selectinload(CorporaORM.speeches))
                .filter(CorporaORM.countries.any(value=country.value))
                .all()
            )
            return [CorporaMapper.to_domain(orm) for orm in orm_corpora]

    def add(self, corpora: Corpora) -> None:
        with session_scope() as session:
            orm_corpora = CorporaMapper.to_orm(corpora)
            
            # Handle many-to-many relationship with speeches
            if corpora.texts:
                speech_ids = [text_id.value for text_id in corpora.texts]
                speeches = session.query(SpeechORM).filter(SpeechORM.id.in_(speech_ids)).all()
                orm_corpora.speeches = speeches
            
            session.add(orm_corpora)

    def update(self, corpora: Corpora) -> None:
        with session_scope() as session:
            exists = session.query(CorporaORM).filter_by(id=corpora.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Corpora with id {corpora.id} not found.")
            
            orm_corpora = CorporaMapper.to_orm(corpora)
            
            # Handle many-to-many relationship with speeches
            if corpora.texts:
                speech_ids = [text_id.value for text_id in corpora.texts]
                speeches = session.query(SpeechORM).filter(SpeechORM.id.in_(speech_ids)).all()
                orm_corpora.speeches = speeches
            else:
                orm_corpora.speeches = []
            
            session.merge(orm_corpora)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_corpora = session.query(CorporaORM).filter_by(id=id.value).one_or_none()
            if orm_corpora:
                session.delete(orm_corpora)
