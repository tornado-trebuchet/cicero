from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from backend.infrastructure.orm.text.orm_speech import SpeechORM

corpora_speeches = Table(
    "corpora_speeches",
    Base.metadata,
    Column(
        "corpora_id",
        PG_UUID(as_uuid=True),
        ForeignKey("corpora.id"),
        primary_key=True,
    ),
    Column(
        "speech_id",
        PG_UUID(as_uuid=True),
        ForeignKey("speeches.id"),
        primary_key=True,
    ),
)

class CorporaORM(Base):
    __tablename__ = "corpora"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    label: Mapped[str] = mapped_column(String, nullable=False)
    countries: Mapped[Optional[List[uuid.UUID]]] = mapped_column(ARRAY(PG_UUID(as_uuid=True)), nullable=True)
    institutions: Mapped[Optional[List[uuid.UUID]]] = mapped_column(
        ARRAY(PG_UUID(as_uuid=True)), nullable=True
    )
    periods: Mapped[Optional[List[uuid.UUID]]] = mapped_column(ARRAY(PG_UUID(as_uuid=True)), nullable=True)
    parties: Mapped[Optional[List[uuid.UUID]]] = mapped_column(ARRAY(PG_UUID(as_uuid=True)), nullable=True)
    speakers: Mapped[Optional[List[uuid.UUID]]] = mapped_column(ARRAY(PG_UUID(as_uuid=True)), nullable=True)

    # Relationships
    speeches: Mapped[List["SpeechORM"]] = relationship(
        "SpeechORM", secondary=corpora_speeches, back_populates="corpora"
    )
