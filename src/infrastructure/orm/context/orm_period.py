from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.types import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
import uuid
from datetime import datetime

class PeriodORM(Base):
    __tablename__ = "periods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
