from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from src.domain.irepository.text.i_speech import ISpeechRepository
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.e_speech_text import SpeechText
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_speech import SpeechORM
from src.infrastructure.orm.text.orm_speech_text import TextORM
from src.infrastructure.orm.text.orm_protocol import ProtocolORM
from src.infrastructure.mappers.text.m_speech import SpeechMapper
from src.infrastructure.mappers.text.m_speech_text import TextMapper


class SpeechRepository(ISpeechRepository):
    """PostgreSQL implementation of the Speech repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Speech]:
        """Get Speech entity by ID."""
        try:
            orm_speech = self._session.query(SpeechORM).options(
                joinedload(SpeechORM.text)
            ).filter(SpeechORM.id == id.value).one()
            
            return self._rehydrate_speech_aggregate(orm_speech)
        except NoResultFound:
            return None
    
    def get_by_protocol_id(self, protocol_id: UUID) -> List[Speech]:
        """Get all speeches for a protocol."""
        orm_speeches = self._session.query(SpeechORM).options(
            joinedload(SpeechORM.text)
        ).filter(SpeechORM.protocol_id == protocol_id.value).all()
        
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def get_by_speaker_id(self, speaker_id: UUID) -> List[Speech]:
        """Get all speeches by a specific speaker."""
        orm_speeches = self._session.query(SpeechORM).options(
            joinedload(SpeechORM.text)
        ).filter(SpeechORM.speaker_id == speaker_id.value).all()
        
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def list(self) -> List[Speech]:
        """List all speeches."""
        orm_speeches = self._session.query(SpeechORM).options(
            joinedload(SpeechORM.text)
        ).order_by(SpeechORM.protocol_id).all()
        
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def add(self, speech: Speech) -> None:
        """Add a new speech aggregate."""
        # Add Speech
        orm_speech = SpeechMapper.to_orm(speech)
        self._session.add(orm_speech)
        self._session.flush()
        
        # Add Text (always new for each speech)
        orm_text = TextMapper.to_orm(speech.text)
        self._session.add(orm_text)
        self._session.flush()
    
    def update(self, speech: Speech) -> None:
        """Update a speech aggregate."""
        # Update Speech
        orm_speech = self._session.query(SpeechORM).filter(
            SpeechORM.id == speech.id.value
        ).one()
        
        # Update speech fields
        orm_speech.protocol_id = speech.protocol_id.value
        orm_speech.speaker_id = speech.speaker_id.value
        
        # Update metrics
        metrics_data = None
        if speech.metrics:
            metrics_data = {
                "dominant_topics": speech.metrics.dominant_topics,
                "sentiment": speech.metrics.sentiment,
                "dynamic_codes": speech.metrics.dynamic_codes
            }
        orm_speech.metrics_data = metrics_data
        orm_speech.metadata_data = speech.metadata._data if speech.metadata else {}
        
        # Update Text
        orm_text = self._session.query(TextORM).filter(
            TextORM.speech_id == speech.id.value
        ).first()
        
        if orm_text:
            # Use TextMapper to properly update ORM from domain
            updated_orm_text = TextMapper.to_orm(speech.text)
            orm_text.language_code = updated_orm_text.language_code
            orm_text.raw_text = updated_orm_text.raw_text
            orm_text.clean_text = updated_orm_text.clean_text
            orm_text.tokens = updated_orm_text.tokens
            orm_text.ngram_tokens = updated_orm_text.ngram_tokens
        
        self._session.flush()
    
    def delete(self, id: UUID) -> None:
        """
        Delete a speech aggregate.
        Will cascade delete Text but preserve Speaker for other speeches.
        """
        orm_speech = self._session.query(SpeechORM).filter(
            SpeechORM.id == id.value
        ).one()
        
        # Delete the speech (Text will cascade delete due to ORM relationship)
        # Speaker is preserved as it may be referenced by other speeches
        self._session.delete(orm_speech)
        self._session.flush()
    
    def get_by_date_range(self, start_date, end_date) -> List[Speech]:
        """Get all speeches whose protocol date is within the given range."""
        orm_speeches = self._session.query(SpeechORM).join(SpeechORM.protocol).options(
            joinedload(SpeechORM.text)
        ).filter(
            ProtocolORM.date >= start_date,
            ProtocolORM.date <= end_date
        ).all()
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]

    def get_by_period(self, period_id: UUID) -> List[Speech]:
        """Get all speeches for a given period (via protocol's period_id)."""
        orm_speeches = self._session.query(SpeechORM).join(SpeechORM.protocol).options(
            joinedload(SpeechORM.text)
        ).filter(
            ProtocolORM.period_id == period_id.value # FIXME: no longer has an ID it's a VO 
        ).all()
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def _rehydrate_speech_aggregate(self, orm_speech: SpeechORM) -> Speech:
        """
        Rehydrate a Speech aggregate from ORM entities.
        Speech aggregate only contains Speech and Text entities.
        """
        # Convert Text
        if not orm_speech.text:
            raise ValueError(f"Speech {orm_speech.id} missing required text")
        
        text = TextMapper.to_domain(orm_speech.text)
        
        # FIXME: SpeechMapper.to_domain needs to be updated to match domain model
        # For now, create Speech directly using domain constructor
        metrics = None
        metrics_data = getattr(orm_speech, 'metrics_data', None)
        if metrics_data:
            from src.domain.models.text.v_speech_metrics_plugin import MetricsPlugin
            metrics = MetricsPlugin(
                dominant_topics=metrics_data.get("dominant_topics", []),
                sentiment=metrics_data.get("sentiment", {}),
                dynamic_codes=metrics_data.get("dynamic_codes", [])
            )
        
        metadata_data = getattr(orm_speech, 'metadata_data', {}) or {}
        from src.domain.models.common.v_metadata_plugin import MetadataPlugin
        
        return Speech(
            id=UUID(str(orm_speech.id)),
            protocol_id=UUID(str(orm_speech.protocol_id)),
            speaker_id=UUID(str(orm_speech.speaker_id)),
            text=text,
            metrics=metrics,
            metadata=MetadataPlugin(metadata_data)
        )