from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy import Text as SQLText, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech import SpeechORM

class SplitTextORM(Base):
    __tablename__ = "split_texts"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("speeches.id"), nullable=False, unique=True)
    sentences: Mapped[List[str]] = mapped_column(ARRAY(SQLText), nullable=False)

    # Relationships
    speech: Mapped["SpeechORM"] = relationship(
        "SpeechORM",
        back_populates="split_text",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_split_text_speech', 'speech_id'),
    )
