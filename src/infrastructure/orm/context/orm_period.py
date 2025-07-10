from __future__ import annotations

from sqlalchemy import Index
from sqlalchemy.types import DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.orm.orm_base import Base
from src.domain.models.common.v_enums import OwnerTypeEnum
from datetime import datetime
import uuid

class PeriodORM(Base):
    __tablename__ = "periods"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    owner_type: Mapped[OwnerTypeEnum] = mapped_column(PG_ENUM(OwnerTypeEnum, name="owner_type_enum"), nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # Indexes for efficient owner lookups
    __table_args__ = (
        Index('idx_period_owner', 'owner_id', 'owner_type'),
        Index('idx_period_dates', 'start_date', 'end_date'),
    )
