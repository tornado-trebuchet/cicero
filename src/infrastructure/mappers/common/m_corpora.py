from typing import Set, Optional, List
from sqlalchemy.orm import Session
from src.domain.models.common.a_corpora import Corpora
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import PartyEnumRegistry
from src.domain.models.context.v_label import Label
from domain.models.context.e_period import Period
from src.infrastructure.orm.common.orm_corpora import CorporaORM


class CorporaMapper:
    """Mapper for converting between Corpora domain model and CorporaORM."""
    
    @staticmethod
    def to_domain(orm_corpora: CorporaORM) -> Corpora:
        """Convert ORM to domain model - WARNING: loads all speeches into memory."""
        # This method should be avoided for large corpora due to memory constraints
        # TODO: Handle SpeechText loading for each speech - requires speech text repository
        speeches = set()  # Placeholder - speech loading requires text parameter
        
        return Corpora(
            id=UUID(str(orm_corpora.id)),
            label=Label(orm_corpora.label),
            speeches=speeches,
            country=orm_corpora.country,
            institution=orm_corpora.institution,
            periods=CorporaMapper._deserialize_periods(orm_corpora.periods),
            party=CorporaMapper._deserialize_party(orm_corpora.party)
        )
    
    @staticmethod
    def to_domain_lazy(orm_corpora: CorporaORM, session: Session) -> Corpora:
        """Convert ORM to domain model with lazy-loaded speeches for memory efficiency."""
        # Create a lazy speech set that loads speeches on demand
        lazy_speeches = LazyLoadedSpeechSet(orm_corpora.speeches, session)
        
        return Corpora(
            id=UUID(str(orm_corpora.id)),
            label=Label(orm_corpora.label),  
            speeches=lazy_speeches,  # TODO: Handle SpeechText loading - requires speech text repository
            country=orm_corpora.country, 
            institution=orm_corpora.institution,
            periods=CorporaMapper._deserialize_periods(orm_corpora.periods),
            party=CorporaMapper._deserialize_party(orm_corpora.party)
        )
    
    @staticmethod
    def to_orm(corpora: Corpora) -> CorporaORM:
        """Convert domain model to ORM - handles speech references efficiently."""
        return CorporaORM(
            id=corpora.id.value,
            label=corpora.label.value,
            country=corpora.country,
            institution=corpora.institution,
            party=CorporaMapper._serialize_party(corpora.party),
            periods=CorporaMapper._serialize_periods(corpora.periods)
            # Note: speeches relationship handled separately for memory efficiency
        )
    
    @staticmethod
    def _serialize_periods(periods: Optional[List[Period]]) -> Optional[List[str]]:
        """Serialize periods to strings for database storage."""
        if periods is None:
            return None
        # TODO: Implement proper Period serialization
        return [str(period) for period in periods]
    
    @staticmethod
    def _deserialize_periods(periods_data: Optional[List[str]]) -> Optional[List[Period]]:
        """Deserialize periods from database strings."""
        if periods_data is None:
            return None
        # TODO: Implement proper Period deserialization - using placeholder for now
        return []  # Placeholder until Period.from_string is implemented
    
    @staticmethod
    def _serialize_party(party: Optional[PartyEnumRegistry]) -> Optional[str]:
        """Serialize party enum to string for database storage."""
        if party is None:
            return None
        return str(party)
    
    @staticmethod
    def _deserialize_party(party_data: Optional[str]) -> Optional[PartyEnumRegistry]:
        """Deserialize party from database string."""
        if party_data is None:
            return None
        # TODO: Implement proper PartyEnumRegistry deserialization - using placeholder for now
        return None  # Placeholder until PartyEnumRegistry.from_string is implemented


class LazyLoadedSpeechSet:
    """A Set-like wrapper that lazy loads speeches to prevent memory exhaustion."""
    
    # TODO: Consider implementing caching for frequently accessed speech subsets
    
    def __init__(self, speeches_query, session: Session):
        self._speeches_query = speeches_query
        self._session = session
        self._cached_speeches: Optional[Set] = None
    
    def __len__(self) -> int:
        """Get count without loading all speeches."""
        return self._speeches_query.count()
    
    def __iter__(self):
        """Iterate over speeches with chunked loading to manage memory."""
        # TODO: Implement chunked iteration for very large collections
        # TODO: Handle SpeechText loading - requires speech text repository integration
        if self._cached_speeches is None:
            self._cached_speeches = set()  # Placeholder - requires SpeechText loading
        return iter(self._cached_speeches)
    
    def __contains__(self, item) -> bool:
        """Check if speech is in the collection."""
        # For efficiency, check by ID rather than loading all speeches
        return self._speeches_query.filter_by(id=item.id.value).first() is not None
    
    def add(self, speech):
        """Add a speech to the collection."""
        # This would require complex handling - mark as TODO
        raise NotImplementedError("TODO: Implement efficient speech addition to lazy set")
    
    def remove(self, speech):
        """Remove a speech from the collection."""
        # This would require complex handling - mark as TODO
        raise NotImplementedError("TODO: Implement efficient speech removal from lazy set") 