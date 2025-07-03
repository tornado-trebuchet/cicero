from typing import List
from sqlalchemy.orm import Session

from domain.irepository.service.i_country_query_service import ICountryQueryService
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.e_party import Party
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.context.orm_institution import InstitutionORM
from src.infrastructure.orm.context.orm_speaker import SpeakerORM
from src.infrastructure.orm.context.orm_party import PartyORM
from src.infrastructure.mappers.context.m_institution import InstitutionMapper
from src.infrastructure.mappers.context.m_speaker import SpeakerMapper
from src.infrastructure.mappers.context.m_party import PartyMapper


class CountryQueryService(ICountryQueryService):
    """PostgreSQL implementation of the Country query service.
    
    This service handles read operations for country-related entities
    without the overhead of loading full aggregates.
    """
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_institutions_by_country(self, country_id: UUID) -> List[Institution]:
        """Get all institutions for a specific country."""
        orm_institutions = self._session.query(InstitutionORM).filter(
            InstitutionORM.country_id == country_id.value
        ).all()
        return [InstitutionMapper.to_domain(orm_institution) for orm_institution in orm_institutions]

    def get_speakers_by_country(self, country_id: UUID) -> List[Speaker]:
        """Get all speakers for a specific country."""
        orm_speakers = self._session.query(SpeakerORM).filter(
            SpeakerORM.country_id == country_id.value
        ).all()
        return [SpeakerMapper.to_domain(orm_speaker) for orm_speaker in orm_speakers]

    def get_parties_by_country(self, country_id: UUID) -> List[Party]:
        """Get all parties for a specific country."""
        orm_parties = self._session.query(PartyORM).filter(
            PartyORM.country_id == country_id.value
        ).all()
        return [PartyMapper.to_domain(orm_party) for orm_party in orm_parties]
    
    def get_speakers_by_party(self, party_id: UUID) -> List[Speaker]:
        """Get all speakers belonging to a specific party."""
        orm_speakers = self._session.query(SpeakerORM).filter(
            SpeakerORM.party_id == party_id.value
        ).all()
        return [SpeakerMapper.to_domain(orm_speaker) for orm_speaker in orm_speakers]
    
    def count_speakers_by_country(self, country_id: UUID) -> int:
        """Get count of speakers for a country without loading all entities."""
        return self._session.query(SpeakerORM).filter(
            SpeakerORM.country_id == country_id.value
        ).count()
    
    def count_parties_by_country(self, country_id: UUID) -> int:
        """Get count of parties for a country without loading all entities."""
        return self._session.query(PartyORM).filter(
            PartyORM.country_id == country_id.value
        ).count()
