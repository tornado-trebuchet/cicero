from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.models.common.v_enums import LanguageEnum
from backend.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from backend.infrastructure.orm.text.orm_speech import SpeechORM
    from backend.infrastructure.orm.text.orm_text_clean import CleanTextORM
    from backend.infrastructure.orm.text.orm_text_ngrams import TextNgramsORM
    from backend.infrastructure.orm.text.orm_text_raw import RawTextORM
    from backend.infrastructure.orm.text.orm_text_split import SplitTextORM
    from backend.infrastructure.orm.text.orm_text_tokenized import TokenizedTextORM
    from backend.infrastructure.orm.text.orm_text_translated import (
        TranslatedTextORM,
    )


class SpeechTextORM(Base):
    __tablename__ = "speech_texts"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    speech_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("speeches.id"),
        nullable=False,
        unique=True,
    )
    language_code: Mapped[LanguageEnum] = mapped_column(
        PG_ENUM(LanguageEnum, name="language_enum"), nullable=True
    )
    metrics: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Relationships
    speech: Mapped["SpeechORM"] = relationship(
        "SpeechORM",
        back_populates="speech_text",
        passive_deletes=True,
        foreign_keys="SpeechTextORM.speech_id",
    )
    clean_text: Mapped[Optional["CleanTextORM"]] = relationship(
        "CleanTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="CleanTextORM.speech_text_id",
    )
    ngram_tokens: Mapped[Optional["TextNgramsORM"]] = relationship(
        "TextNgramsORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="TextNgramsORM.speech_text_id",
    )
    raw_text: Mapped["RawTextORM"] = relationship(
        "RawTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="RawTextORM.speech_text_id",
    )
    sentences: Mapped[Optional["SplitTextORM"]] = relationship(
        "SplitTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="SplitTextORM.speech_text_id",
    )
    tokens: Mapped[Optional["TokenizedTextORM"]] = relationship(
        "TokenizedTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="TokenizedTextORM.speech_text_id",
    )
    translated_text: Mapped[Optional["TranslatedTextORM"]] = relationship(
        "TranslatedTextORM",
        back_populates="speech_text",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="TranslatedTextORM.speech_text_id",
    )
    __table_args__ = (Index("idx_text_speech", "speech_id"),)
