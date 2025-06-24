"""
PostgreSQL implementation of the Country repository.

"""


from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.domain.irepository.i_country import ICountryRepository
from src.domain.models.e_country import Country
from src.domain.models.v_common import UUID
from src.domain.models.v_enums import CountryEnum
from src.infrastructure.orm.orm_country import CountryORM
from src.infrastructure.mappers.m_country import CountryMapper


class CountryRepository(ICountryRepository):
    """PostgreSQL implementation of the Country repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Country]:
        """Get country by ID."""
        try:
            orm_country = self._session.query(CountryORM).filter(
                CountryORM.id == id.value
            ).one()
            return CountryMapper.to_domain(orm_country)
        except NoResultFound:
            return None
    
    def get_by_country_enum(self, country: CountryEnum) -> Optional[Country]:
        """Get country by country enum value."""
        try:
            orm_country = self._session.query(CountryORM).filter(
                CountryORM.name == country
            ).one()
            return CountryMapper.to_domain(orm_country)
        except NoResultFound:
            return None
    
    def list(self) -> List[Country]:
        """List all countries."""
        orm_countries = self._session.query(CountryORM).order_by(CountryORM.name).all()
        return [CountryMapper.to_domain(orm_country) for orm_country in orm_countries]
    
    def add(self, country: Country) -> None:
        """Add a new country."""
        orm_country = CountryMapper.to_orm(country)
        self._session.add(orm_country)
        self._session.flush()  # Ensure ID is generated
    
    def update(self, country: Country) -> None:
        """Update a country."""
        orm_country = self._session.query(CountryORM).filter(
            CountryORM.id == country.id.value
        ).one()
        
        # Update fields
        orm_country.name = country.country
        
        self._session.flush()
    
    def delete(self, id: UUID) -> None:
        """Delete a country (will cascade delete institutions)."""
        orm_country = self._session.query(CountryORM).filter(
            CountryORM.id == id.value
        ).one()
        
        self._session.delete(orm_country)
        self._session.flush()