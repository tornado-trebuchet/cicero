from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infrastructure.orm.base_orm import Base
from src.domain.models.common.v_enums import CountryEnum
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_institution import InstitutionORM
    from src.infrastructure.orm.context.orm_speaker import SpeakerORM
    from src.infrastructure.orm.context.orm_party import PartyORM
    from src.infrastructure.orm.context.orm_period import PeriodORM

class CountryORM(Base):
    __tablename__ = "countries"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    country: Mapped[CountryEnum] = mapped_column(PG_ENUM(CountryEnum, name="country_enum"), nullable=False, unique=True)

    # Relationships
    periodisation: Mapped[List["PeriodORM"]] = relationship(
        "PeriodORM",
        back_populates="country",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    institutions: Mapped[List["InstitutionORM"]] = relationship(
        "InstitutionORM", 
        back_populates="country",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    speakers: Mapped[List["SpeakerORM"]] = relationship(
        "SpeakerORM",
        back_populates="country",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    parties: Mapped[List["PartyORM"]] = relationship(
        "PartyORM",
        back_populates="country",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

