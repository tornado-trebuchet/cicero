from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Dict, List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_country import CountryORM
    from src.infrastructure.orm.text.orm_protocol import ProtocolORM


class InstitutionORM(Base):
    __tablename__ = "institutions"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True
    )
    country_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False
    )
    institution_type: Mapped[InstitutionTypeEnum] = mapped_column(
        PG_ENUM(InstitutionTypeEnum, name="institution_type_enum"),
        nullable=False,
    )
    label: Mapped[str] = mapped_column(nullable=False)
    meta_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Relationships
    country: Mapped["CountryORM"] = relationship(
        "CountryORM", back_populates="institutions"
    )
    protocols: Mapped[List["ProtocolORM"]] = relationship(
        "ProtocolORM",
        back_populates="institution",
    )
