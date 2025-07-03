from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Text, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_country import CountryORM
    from src.infrastructure.orm.context.orm_speaker import SpeakerORM

class PartyORM(Base):
    __tablename__ = "parties"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    country_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    party_enum_value: Mapped[str] = mapped_column(String, nullable=False)  # Stores the enum value string; enum type determined by country
    party_program: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    country: Mapped["CountryORM"] = relationship(
        "CountryORM",
        back_populates="parties"
    )
    members: Mapped[List["SpeakerORM"]] = relationship(
        "SpeakerORM",
        back_populates="party_ref",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_party_country', 'country_id'),
        Index('idx_party_enum', 'party_enum_value'),
        Index('idx_party_country_enum', 'country_id', 'party_enum_value', unique=True),
    )