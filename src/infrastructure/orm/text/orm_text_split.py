from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy import Text as SQLText, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech_text import TextORM

class SplitTextORM(Base):
    __tablename__ = "split_texts"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_text_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("texts.id"), nullable=False, unique=True)
    sentences: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)

    # Relationships
    speech_text: Mapped["TextORM"] = relationship(
        "TextORM",
        back_populates="sentences",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False
    )

    __table_args__ = (
        Index('idx_split_text_speech_text', 'speech_text_id'),
    )
