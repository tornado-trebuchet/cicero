from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index
from sqlalchemy import Text as SQLText
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM


class RawTextORM(Base):
    __tablename__ = "raw_texts"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_text_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("speech_texts.id"),
        nullable=False,
        unique=True,
    )
    text: Mapped[str] = mapped_column(SQLText, nullable=False)

    # Relationships
    speech_text: Mapped["SpeechTextORM"] = relationship(
        "SpeechTextORM",
        back_populates="raw_text",
        passive_deletes=True,
        uselist=False,
    )

    __table_args__ = (Index("idx_raw_text_speech_text", "speech_text_id"),)
