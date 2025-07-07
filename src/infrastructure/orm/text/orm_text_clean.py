from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Text as SQLText, Integer, ForeignKey, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech import SpeechORM

class CleanTextORM(Base):
    __tablename__ = "clean_texts"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("speeches.id"), nullable=False, unique=True)
    clean_text: Mapped[str] = mapped_column(SQLText, nullable=False)

    # Relationships
    speech: Mapped["SpeechORM"] = relationship(
        "SpeechORM",
        back_populates="clean_text",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_clean_text_speech', 'speech_id'),
    )
