# filepath: /home/janeendaredevil/LocalCode/cicero/src/infrastructure/repository/pgsql/rep_speech.py
"""
PostgreSQL implementation of the Speech repository.
Speech is an aggregate that requires full rehydration with Speaker and Text entities.
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from domain.irepository.text.i_speech import ISpeechRepository
from domain.models.text.e_speech import Speech
from domain.models.context.ve_speaker import Speaker
from domain.models.text.ve_text import Text
from domain.models.common.v_common import UUID
from infrastructure.orm.text.orm_speech import SpeechORM
from infrastructure.orm.context.orm_speaker import SpeakerORM
from infrastructure.orm.text.orm_text import TextORM
from infrastructure.orm.text.orm_protocol import ProtocolORM
from infrastructure.mappers.text.m_speech import SpeechMapper
from infrastructure.mappers.context.m_speaker import SpeakerMapper
from infrastructure.mappers.text.m_text import TextMapper


class SpeechRepository(ISpeechRepository):
    """PostgreSQL implementation of the Speech repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Speech]:
        """Get fully rehydrated Speech with Speaker and Text entities."""
        try:
            # Load speech with related entities using joinedload for efficiency
            orm_speech = self._session.query(SpeechORM).options(
                joinedload(SpeechORM.author),
                joinedload(SpeechORM.text)
            ).filter(SpeechORM.id == id.value).one()
            
            return self._rehydrate_speech_aggregate(orm_speech)
        except NoResultFound:
            return None
    
    def get_by_protocol_id(self, protocol_id: UUID) -> List[Speech]:
        """Get all fully rehydrated speeches for a protocol."""
        orm_speeches = self._session.query(SpeechORM).options(
            joinedload(SpeechORM.author),
            joinedload(SpeechORM.text)
        ).filter(SpeechORM.protocol_id == protocol_id.value).all()
        
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def get_by_speaker_id(self, speaker_id: UUID) -> List[Speech]:
        """Get all fully rehydrated speeches by a specific speaker."""
        orm_speeches = self._session.query(SpeechORM).options(
            joinedload(SpeechORM.author),
            joinedload(SpeechORM.text)
        ).filter(SpeechORM.author_id == speaker_id.value).all()
        
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def list(self) -> List[Speech]:
        """List all fully rehydrated speeches."""
        orm_speeches = self._session.query(SpeechORM).options(
            joinedload(SpeechORM.author),
            joinedload(SpeechORM.text)
        ).order_by(SpeechORM.protocol_id).all()
        
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def add(self, speech: Speech) -> None:
        """
        Add a new speech aggregate.
        Will persist Speech, Speaker, and Text entities as a transaction.
        """
        # Handle Speaker (may already exist)
        existing_speaker = self._session.query(SpeakerORM).filter(
            SpeakerORM.id == speech.author.id.value
        ).first()
        
        if not existing_speaker:
            # Add new speaker
            orm_speaker = SpeakerMapper.to_orm(speech.author)
            self._session.add(orm_speaker)
            self._session.flush()
        else:
            # Update existing speaker if needed
            existing_speaker.name = speech.author.name
            existing_speaker.party = str(speech.author.party) if speech.author.party else None
            existing_speaker.role = speech.author.role
            existing_speaker.birth_date = speech.author.birth_date
            existing_speaker.gender = speech.author.gender
        
        # Add Speech
        orm_speech = SpeechMapper.to_orm(speech)
        self._session.add(orm_speech)
        self._session.flush()
        
        # Add Text (always new for each speech)
        orm_text = TextMapper.to_orm(speech.text)
        self._session.add(orm_text)
        self._session.flush()
    
    def update(self, speech: Speech) -> None:
        """
        Update a speech aggregate.
        Will update Speech, Speaker, and Text entities as needed.
        """
        # Update Speech
        orm_speech = self._session.query(SpeechORM).filter(
            SpeechORM.id == speech.id.value
        ).one()
        
        # Update speech fields
        orm_speech.protocol_id = speech.protocol_id.value
        orm_speech.author_id = speech.author.id.value
        
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
        
        # Update Speaker (if it exists)
        orm_speaker = self._session.query(SpeakerORM).filter(
            SpeakerORM.id == speech.author.id.value
        ).first()
        
        if orm_speaker:
            orm_speaker.name = speech.author.name
            orm_speaker.party = str(speech.author.party) if speech.author.party else None
            orm_speaker.role = speech.author.role
            orm_speaker.birth_date = speech.author.birth_date
            orm_speaker.gender = speech.author.gender
        
        # Update Text
        orm_text = self._session.query(TextORM).filter(
            TextORM.speech_id == speech.id.value
        ).first()
        
        if orm_text:
            orm_text.language_code = speech.text.language_code
            orm_text.raw_text = speech.text.raw_text
            orm_text.clean_text = speech.text.clean_text
            orm_text.tokens = speech.text.tokens
            orm_text.ngram_tokens = speech.text.ngram_tokens
            orm_text.word_count = speech.text.word_count
        
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
            joinedload(SpeechORM.author),
            joinedload(SpeechORM.text)
        ).filter(
            ProtocolORM.date >= start_date,
            ProtocolORM.date <= end_date
        ).all()
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]

    def get_by_period(self, period_id: UUID) -> List[Speech]:
        """Get all speeches for a given period (via protocol's period_id)."""
        orm_speeches = self._session.query(SpeechORM).join(SpeechORM.protocol).options(
            joinedload(SpeechORM.author),
            joinedload(SpeechORM.text)
        ).filter(
            ProtocolORM.period_id == period_id.value
        ).all()
        return [self._rehydrate_speech_aggregate(orm_speech) for orm_speech in orm_speeches]
    
    def _rehydrate_speech_aggregate(self, orm_speech: SpeechORM) -> Speech:
        """
        Rehydrate a full Speech aggregate from ORM entities.
        This ensures all dependent entities are properly loaded and converted.
        """
        # Convert Speaker
        if not orm_speech.author:
            raise ValueError(f"Speech {orm_speech.id} missing required author")
        
        speaker = SpeakerMapper.to_domain(orm_speech.author)
        
        # Convert Text
        text = None
        if orm_speech.text:
            text = TextMapper.to_domain(orm_speech.text)
        else:
            raise ValueError(f"Speech {orm_speech.id} missing required text")
        
        # Convert Speech with aggregated entities
        return SpeechMapper.to_domain(orm_speech, speaker, text)