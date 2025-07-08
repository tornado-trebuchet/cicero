from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Text as SQLText, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM

class CleanTextORM(Base):
    __tablename__ = "clean_texts"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_text_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("speech_texts.id", ondelete="CASCADE"), nullable=False, unique=True)
    clean_text: Mapped[str] = mapped_column(SQLText, nullable=False)

    # Relationships
    speech_text: Mapped["SpeechTextORM"] = relationship(
        "SpeechTextORM",
        back_populates="clean_text",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False
    )

    __table_args__ = (
        Index('idx_clean_text_speech_text', 'speech_text_id'),
    )
