"""
PostgreSQL implementation of the RegexPattern repository.
RegexPattern references Country, Institution, and optionally Period but doesn't own them.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc

from src.domain.irepository.i_regex_pattern import IRegexPatternRepository
from src.domain.models.e_regex_pattern import RegexPattern
from src.domain.models.v_common import UUID
from src.infrastructure.orm.orm_regex_pattern import RegexPatternORM
from src.infrastructure.mappers.m_regex_pattern import RegexPatternMapper


class RegexPatternRepository(IRegexPatternRepository):
    """PostgreSQL implementation of the RegexPattern repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[RegexPattern]:
        """Get regex pattern by ID."""
        try:
            orm_pattern = self._session.query(RegexPatternORM).filter(
                RegexPatternORM.id == id.value
            ).one()
            return RegexPatternMapper.to_domain(orm_pattern)
        except NoResultFound:
            return None
    
    def get_active_by_scope(self, country_id: UUID, institution_id: UUID, period_id: Optional[UUID] = None) -> List[RegexPattern]:
        """Get active regex patterns for a specific scope (country, institution, optional period)."""
        query = self._session.query(RegexPatternORM).filter(
            RegexPatternORM.country_id == country_id.value,
            RegexPatternORM.institution_id == institution_id.value,
            RegexPatternORM.is_active == True
        )
        
        if period_id:
            query = query.filter(RegexPatternORM.period_id == period_id.value)
        else:
            # If no period specified, get patterns with no period constraint
            query = query.filter(RegexPatternORM.period_id.is_(None))
        
        orm_patterns = query.order_by(desc(RegexPatternORM.version)).all()
        return [RegexPatternMapper.to_domain(orm_pattern) for orm_pattern in orm_patterns]
    
    def get_by_country_and_institution(self, country_id: UUID, institution_id: UUID) -> List[RegexPattern]:
        """Get all regex patterns for a country and institution."""
        orm_patterns = self._session.query(RegexPatternORM).filter(
            RegexPatternORM.country_id == country_id.value,
            RegexPatternORM.institution_id == institution_id.value
        ).order_by(
            RegexPatternORM.period_id.nulls_first(),
            desc(RegexPatternORM.version),
            desc(RegexPatternORM.is_active)
        ).all()
        
        return [RegexPatternMapper.to_domain(orm_pattern) for orm_pattern in orm_patterns]
    
    def get_latest_version_by_scope(self, country_id: UUID, institution_id: UUID, period_id: Optional[UUID] = None) -> Optional[RegexPattern]:
        """Get the latest version of regex pattern for a scope."""
        query = self._session.query(RegexPatternORM).filter(
            RegexPatternORM.country_id == country_id.value,
            RegexPatternORM.institution_id == institution_id.value
        )
        
        if period_id:
            query = query.filter(RegexPatternORM.period_id == period_id.value)
        else:
            query = query.filter(RegexPatternORM.period_id.is_(None))
        
        try:
            orm_pattern = query.order_by(desc(RegexPatternORM.version)).first()
            return RegexPatternMapper.to_domain(orm_pattern) if orm_pattern else None
        except NoResultFound:
            return None
    
    def list(self) -> List[RegexPattern]:
        """List all regex patterns."""
        orm_patterns = self._session.query(RegexPatternORM).order_by(
            RegexPatternORM.country_id,
            RegexPatternORM.institution_id,
            RegexPatternORM.period_id.nulls_first(),
            desc(RegexPatternORM.version)
        ).all()
        
        return [RegexPatternMapper.to_domain(orm_pattern) for orm_pattern in orm_patterns]
    
    def add(self, regex_pattern: RegexPattern) -> None:
        """Add a new regex pattern."""
        orm_pattern = RegexPatternMapper.to_orm(regex_pattern)
        self._session.add(orm_pattern)
        self._session.flush()  # Ensure ID is generated
    
    def update(self, regex_pattern: RegexPattern) -> None:
        """Update a regex pattern."""
        orm_pattern = self._session.query(RegexPatternORM).filter(
            RegexPatternORM.id == regex_pattern.id.value
        ).one()
        
        # Update fields
        orm_pattern.country_id = regex_pattern.country.value
        orm_pattern.institution_id = regex_pattern.institution.value
        orm_pattern.period_id = regex_pattern.period.value if regex_pattern.period else None
        orm_pattern.pattern = regex_pattern.pattern
        orm_pattern.description = regex_pattern.description
        orm_pattern.version = regex_pattern.version if regex_pattern.version else 1
        orm_pattern.is_active = regex_pattern.is_active
        
        self._session.flush()
    
    def delete(self, id: UUID) -> None:
        """Delete a regex pattern."""
        orm_pattern = self._session.query(RegexPatternORM).filter(
            RegexPatternORM.id == id.value
        ).one()
        
        self._session.delete(orm_pattern)
        self._session.flush()