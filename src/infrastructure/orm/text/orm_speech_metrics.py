from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech import SpeechORM


class SpeechMetricsORM(Base):
    __tablename__ = "speech_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True
    )
    speech_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("speeches.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    dominant_topics: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(
        JSONB, nullable=True
    )
    sentiment: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    dynamic_codes: Mapped[Optional[List[Any]]] = mapped_column(
        JSONB, nullable=True
    )

    # Relationships
    speech: Mapped["SpeechORM"] = relationship(
        "SpeechORM",
        back_populates="speech_metrics",
        passive_deletes=True,
        uselist=False,
    )

    __table_args__ = (Index("idx_speech_metrics_speech", "speech_id"),)
