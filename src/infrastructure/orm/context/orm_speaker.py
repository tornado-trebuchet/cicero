from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Date, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infrastructure.orm.base import Base
from src.domain.models.common.v_enums import GenderEnum
from datetime import date
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech import SpeechORM
    from src.infrastructure.orm.context.orm_country import CountryORM
    from src.infrastructure.orm.context.orm_party import PartyORM

class SpeakerORM(Base):
    __tablename__ = "speakers"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    country_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False)
    party_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("parties.id"), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(PG_ENUM(GenderEnum, name="gender_enum"), nullable=True)
    
    # Relationships
    country: Mapped["CountryORM"] = relationship(
        "CountryORM",
        back_populates="speakers",
        passive_deletes=True
    )
    party_ref: Mapped[Optional["PartyORM"]] = relationship(
        "PartyORM",
        back_populates="members",
        passive_deletes=True
    )
    speeches: Mapped[List["SpeechORM"]] = relationship(
        "SpeechORM",
        back_populates="speaker",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_speaker_party_id', 'party_id'),
        Index('idx_speaker_name', 'name'),
    )
