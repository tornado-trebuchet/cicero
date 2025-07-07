from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import DateTime, String

from src.infrastructure.orm.base_orm import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_country import CountryORM
    from src.infrastructure.orm.context.orm_institution import InstitutionORM

class PeriodORM(Base):
    __tablename__ = "periods"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("countries.id"), nullable=True)
    institution_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=True)
    label: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    country: Mapped[Optional["CountryORM"]] = relationship(
        "CountryORM",
        back_populates="periodisation",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    institution: Mapped[Optional["InstitutionORM"]] = relationship(
        "InstitutionORM",
        back_populates="periods",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_period_institution', 'institution_id'),
    )
