from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_country import CountryORM
    from src.infrastructure.orm.context.orm_speaker import SpeakerORM


class PartyORM(Base):
    __tablename__ = "parties"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    country_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False
    )
    label: Mapped[str] = mapped_column(String, nullable=False)
    party_name: Mapped[str] = mapped_column(String, nullable=False)
    party_program: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    country: Mapped["CountryORM"] = relationship("CountryORM", back_populates="parties", passive_deletes=True)
    members: Mapped[List["SpeakerORM"]] = relationship(
        "SpeakerORM",
        back_populates="party_ref",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
