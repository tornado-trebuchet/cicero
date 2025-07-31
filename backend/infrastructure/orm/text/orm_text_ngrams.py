from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from backend.infrastructure.orm.text.orm_speech_text import SpeechTextORM


class TextNgramsORM(Base):
    __tablename__ = "text_ngrams"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_text_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("speech_texts.id"),
        nullable=False,
        unique=True,
    )
    ngram_tokens: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)

    # Relationships
    speech_text: Mapped["SpeechTextORM"] = relationship(
        "SpeechTextORM",
        back_populates="ngram_tokens",
        passive_deletes=True,
        uselist=False,
    )

    __table_args__ = (Index("idx_text_ngrams_speech_text", "speech_text_id"),)
