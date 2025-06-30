from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
import uuid

if TYPE_CHECKING:
    from infrastructure.orm.text.orm_protocol import ProtocolORM
    from infrastructure.orm.context.orm_speaker import SpeakerORM
    from infrastructure.orm.text.orm_text import TextORM

class SpeechORM(Base):
    __tablename__ = "speeches"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    protocol_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("protocols.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("speakers.id", ondelete="CASCADE"), nullable=False)
    metrics_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    metadata_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    
    # Relationships
    protocol: Mapped["ProtocolORM"] = relationship(
        "ProtocolORM", 
        back_populates="speeches"
    )
    author: Mapped["SpeakerORM"] = relationship(
        "SpeakerORM", 
        back_populates="speeches"
    )
    text: Mapped[Optional["TextORM"]] = relationship(
        "TextORM", 
        back_populates="speech", 
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_speech_protocol', 'protocol_id'),
        Index('idx_speech_author', 'author_id'),
        Index('idx_speech_protocol_author', 'protocol_id', 'author_id'),
    )
    