from domain.irepository.common.i_corpora import ICorporaRepository
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.domain.models.common.a_corpora import Corpora
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum
from src.infrastructure.orm.common.orm_corpora import CorporaORM
from src.infrastructure.mappers.common.m_corpora import CorporaMapper


class CorporaRepository(ICorporaRepository):
    """PostgreSQL implementation of the Corpora repository with memory-efficient handling."""
    
    # TODO: Add database indexes for performance optimization (country, institution, periods)
    # TODO: Consider implementing caching mechanisms for frequently accessed corpora
    # TODO: Implement batch loading strategies for large speech collections
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Corpora]:
        """Get corpora by ID with lazy-loaded speeches to handle memory constraints."""
        try:
            orm_corpora = self._session.query(CorporaORM).filter(
                CorporaORM.id == id.value
            ).one()
            # Use lazy loading mapper variant to avoid loading all speeches at once
            return CorporaMapper.to_domain_lazy(orm_corpora, self._session)
        except NoResultFound:
            return None
    
    def list_by_country(self, country: CountryEnum) -> List[Corpora]:
        """List all corpora for a given country with memory-efficient loading."""
        orm_corpora_list = self._session.query(CorporaORM).filter(
            CorporaORM.country == country
        ).order_by(CorporaORM.label).all()
        
        # Use lazy loading to prevent memory exhaustion with large speech collections
        return [
            CorporaMapper.to_domain_lazy(orm_corpora, self._session) 
            for orm_corpora in orm_corpora_list
        ]
    
    def add(self, corpora: Corpora) -> None:
        """Add a new corpora aggregate to the repository."""
        # NOTE: Due to memory constraints, speeches should be persisted separately
        # and only references stored in corpora
        orm_corpora = CorporaMapper.to_orm(corpora)
        self._session.add(orm_corpora)
        self._session.flush()
    
    def remove(self, id: UUID) -> None:
        """Remove a corpora aggregate by its unique ID."""
        try:
            orm_corpora = self._session.query(CorporaORM).filter(
                CorporaORM.id == id.value
            ).one()
            self._session.delete(orm_corpora)
            self._session.flush()
        except NoResultFound:
            # Silently handle case where corpora doesn't exist
            pass