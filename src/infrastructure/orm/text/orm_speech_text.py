from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import String, Integer, Text as SQLText, ForeignKey, ARRAY, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
from src.domain.models.common.v_enums import LanguageEnum
import uuid

if TYPE_CHECKING:
    from infrastructure.orm.text.orm_speech import SpeechORM

class TextORM(Base):
    __tablename__ = "texts"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("speeches.id", ondelete="CASCADE"), nullable=False, unique=True)
    language_code: Mapped[Optional[LanguageEnum]] = mapped_column(PG_ENUM(LanguageEnum, name="language_enum"), nullable=True)
    raw_text: Mapped[str] = mapped_column(SQLText, nullable=False)
    clean_text: Mapped[Optional[str]] = mapped_column(SQLText, nullable=True)
    tokens: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    ngram_tokens: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    # TODO: add translated text from domain model and check if it is properly integrated 
    translated_text: Mapped[Optional[str]] = mapped_column(SQLText, nullable=True)
    word_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # fucking idiot mutated it here to 0, I'll fucking eat your firstborn if that repeats again
    
    # Relationships
    speech: Mapped["SpeechORM"] = relationship(
        "SpeechORM", 
        back_populates="text"
    )

    __table_args__ = (
        CheckConstraint('word_count >= 0', name='check_word_count_positive'), # TF is this?
        Index('idx_text_speech', 'speech_id'),
        Index('idx_text_language', 'language_code'),
        Index('idx_text_word_count', 'word_count'),
    )
    
