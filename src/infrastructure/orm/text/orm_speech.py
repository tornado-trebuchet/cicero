from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from src.infrastructure.orm.common.orm_corpora import CorporaORM
    from src.infrastructure.orm.context.orm_speaker import SpeakerORM
    from src.infrastructure.orm.text.orm_protocol import ProtocolORM
    from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM
    from src.infrastructure.orm.text.orm_speech_metrics import SpeechMetricsORM


class SpeechORM(Base):
    __tablename__ = "speeches"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    protocol_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("protocols.id"), nullable=False
    )
    protocol_order: Mapped[int] = mapped_column(nullable=False)
    speaker_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("speakers.id"), nullable=False
    )
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
    speech_text: Mapped["SpeechTextORM"] = relationship(
        "SpeechTextORM", back_populates="speech", uselist=False
    )
    speech_metrics: Mapped[Optional["SpeechMetricsORM"]] = relationship(
        "SpeechMetricsORM", back_populates="speech", uselist=False
    )
    corpora: Mapped[List["CorporaORM"]] = relationship(
        "CorporaORM", secondary="corpora_speeches", back_populates="speeches"
    )

    __table_args__ = (
        Index("idx_speech_protocol", "protocol_id"),
        Index("idx_speech_speaker", "speaker_id"),
    )
