from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from datetime import date
from sqlalchemy import String, Date, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
from src.domain.models.common.v_enums import GenderEnum
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech import SpeechORM
    from src.infrastructure.orm.context.orm_country import CountryORM
    from src.infrastructure.orm.context.orm_party import PartyORM
# All type safety and constraints are handled in the domain model
class SpeakerORM(Base):
    __tablename__ = "speakers"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    country_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    party_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("parties.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False) # Name domain object
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(PG_ENUM(GenderEnum, name="gender_enum"), nullable=True)
    
    # Relationships
    country: Mapped["CountryORM"] = relationship(
        "CountryORM",
        back_populates="speakers"
    )
    party_ref: Mapped[Optional["PartyORM"]] = relationship(
        "PartyORM",
        back_populates="members"
    )
    speeches: Mapped[List["SpeechORM"]] = relationship(
        "SpeechORM",
        back_populates="speaker",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_speaker_country', 'country_id'),
        Index('idx_speaker_party_id', 'party_id'),
        Index('idx_speaker_name', 'name'),
        Index('idx_speaker_name_party', 'name', 'party_id'),
    )
