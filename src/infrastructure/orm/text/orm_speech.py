from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict, Any, List

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infrastructure.orm.orm_base import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_protocol import ProtocolORM
    from src.infrastructure.orm.context.orm_speaker import SpeakerORM
    from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM
    from src.infrastructure.orm.common.orm_corpora import CorporaORM

class SpeechORM(Base):
    __tablename__ = "speeches"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    protocol_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("protocols.id"), nullable=False)
    speaker_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("speakers.id"), nullable=False)
    metrics_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    meta_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    
    # Relationships
    protocol: Mapped["ProtocolORM"] = relationship(
        "ProtocolORM", 
        back_populates="speeches",
    )
    speaker: Mapped["SpeakerORM"] = relationship(
        "SpeakerORM", 
        back_populates="speeches",
    )
    text: Mapped["SpeechTextORM"] = relationship(
        "SpeechTextORM", 
        back_populates="speech", 
        uselist=False,
        passive_deletes=True
    )

    corpora: Mapped[List["CorporaORM"]] = relationship(
        "CorporaORM",
        secondary="corpora_speeches",
        back_populates="speeches"
    )

    __table_args__ = (
        Index('idx_speech_protocol', 'protocol_id'),
        Index('idx_speech_speaker', 'speaker_id'),
    )
