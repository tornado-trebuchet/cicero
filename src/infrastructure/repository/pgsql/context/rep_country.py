from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from src.domain.irepository.context.i_country import ICountryRepository
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.e_party import Party
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum
from src.infrastructure.orm.context.orm_country import CountryORM
from src.infrastructure.orm.context.orm_institution import InstitutionORM
from src.infrastructure.orm.context.orm_speaker import SpeakerORM
from src.infrastructure.orm.context.orm_party import PartyORM
from src.infrastructure.mappers.context.m_country import CountryMapper
from src.infrastructure.mappers.context.m_institution import InstitutionMapper
from src.infrastructure.mappers.context.m_speaker import SpeakerMapper
from src.infrastructure.mappers.context.m_party import PartyMapper


class CountryRepository(ICountryRepository):
    """PostgreSQL implementation of the Country repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Country]:
        """Get country by ID."""
        try:
            orm_country = self._session.query(CountryORM).options(
                joinedload(CountryORM.institutions),
                joinedload(CountryORM.speakers),
                joinedload(CountryORM.parties)
            ).filter(CountryORM.id == id.value).one()
            return self._rehydrate_country_aggregate(orm_country)
        except NoResultFound:
            return None
    
    def get_by_country_enum(self, country: CountryEnum) -> Optional[Country]:
        """Get country by country enum value."""
        try:
            orm_country = self._session.query(CountryORM).options(
                joinedload(CountryORM.institutions),
                joinedload(CountryORM.speakers),
                joinedload(CountryORM.parties)
            ).filter(CountryORM.name == country).one()
            return self._rehydrate_country_aggregate(orm_country)
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
        self._session.flush()
    
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

    def get_institutions(self, country_id: UUID) -> List[Institution]:
        """Get institutions for a specific country."""
        orm_institutions = self._session.query(InstitutionORM).filter(
            InstitutionORM.country_id == country_id.value
        ).all()
        return [InstitutionMapper.to_domain(orm_institution) for orm_institution in orm_institutions]

    def get_speakers(self, country_id: UUID) -> List[Speaker]:
        """Get speakers for a specific country."""
        orm_speakers = self._session.query(SpeakerORM).filter(
            SpeakerORM.country_id == country_id.value
        ).all()
        return [SpeakerMapper.to_domain(orm_speaker) for orm_speaker in orm_speakers]

    def get_parties(self, country_id: UUID) -> List[Party]:
        """Get parties for a specific country."""
        orm_parties = self._session.query(PartyORM).filter(
            PartyORM.country_id == country_id.value
        ).all()
        return [PartyMapper.to_domain(orm_party) for orm_party in orm_parties]

    def _rehydrate_country_aggregate(self, orm_country: CountryORM) -> Country:
        """
        Rehydrate a Country aggregate from ORM entities.
        Country aggregate contains the country and its related institutions, speakers, and parties.
        """
        # Convert related entities
        institutions = [InstitutionMapper.to_domain(inst) for inst in orm_country.institutions]
        speakers = [SpeakerMapper.to_domain(speaker) for speaker in orm_country.speakers]
        parties = [PartyMapper.to_domain(party) for party in orm_country.parties]

        # Create the Country aggregate with all relationships using the enhanced mapper method
        return CountryMapper.to_domain_with_relationships(
            orm_country,
            institutions=institutions,
            speakers=speakers,
            parties=parties
        )