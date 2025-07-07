from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
from src.domain.models.common.v_enums import LanguageEnum
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech import SpeechORM
    from src.infrastructure.orm.text.orm_text_clean import CleanTextORM
    from src.infrastructure.orm.text.orm_text_ngrams import TextNgramsORM
    from src.infrastructure.orm.text.orm_text_raw import RawTextORM
    from src.infrastructure.orm.text.orm_text_split import SplitTextORM
    from src.infrastructure.orm.text.orm_text_tokenized import TokenizedTextORM
    from src.infrastructure.orm.text.orm_text_translated import TranslatedTextORM

class TextORM(Base):
    __tablename__ = "texts"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("speeches.id"), nullable=False, unique=True)
    raw_text_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    language_code: Mapped[LanguageEnum] = mapped_column(PG_ENUM(LanguageEnum, name="language_enum"), nullable=True)
    clean_text_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    translated_text_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    sentences_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    tokens_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    ngram_tokens_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    metrics: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    speech: Mapped["SpeechORM"] = relationship(
        "SpeechORM", 
        back_populates="text",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    clean_text: Mapped[Optional["CleanTextORM"]] = relationship(
        "CleanTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="CleanTextORM.speech_text_id"
    )
    ngram_tokens: Mapped[Optional["TextNgramsORM"]] = relationship(
        "TextNgramsORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="TextNgramsORM.speech_text_id"
    )
    raw_text: Mapped[Optional["RawTextORM"]] = relationship(
        "RawTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="RawTextORM.speech_text_id"
    )
    sentences: Mapped[Optional["SplitTextORM"]] = relationship(
        "SplitTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="SplitTextORM.speech_text_id"
    )
    tokens: Mapped[Optional["TokenizedTextORM"]] = relationship(
        "TokenizedTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="TokenizedTextORM.speech_text_id"
    )
    translated_text: Mapped[Optional["TranslatedTextORM"]] = relationship(
        "TranslatedTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="TranslatedTextORM.speech_text_id"
    )
    __table_args__ = (
        Index('idx_text_speech', 'speech_id'),
    )

