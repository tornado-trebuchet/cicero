from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from datetime import date
from sqlalchemy import String, Date, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
from domain.models.common.v_enums import GenderEnum
import uuid

if TYPE_CHECKING:
    from infrastructure.orm.text.orm_speech import SpeechORM

class SpeakerORM(Base):
    __tablename__ = "speakers"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    party: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(PG_ENUM(GenderEnum, name="gender_enum"), nullable=True)
    
    # Relationships
    speeches: Mapped[List["SpeechORM"]] = relationship(
        "SpeechORM",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_speaker_name', 'name'),
        Index('idx_speaker_party', 'party'),
        Index('idx_speaker_name_party', 'name', 'party'),
    )
