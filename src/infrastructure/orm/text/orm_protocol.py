from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.common.v_enums import ProtocolTypeEnum
from src.infrastructure.orm.orm_base import Base

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_institution import InstitutionORM
    from src.infrastructure.orm.text.orm_speech import SpeechORM


class ProtocolORM(Base):
    __tablename__ = "protocols"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=False
    )
    label: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    agenda: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    file_source: Mapped[str] = mapped_column(String, nullable=False)
    protocol_type: Mapped[ProtocolTypeEnum] = mapped_column(
        PG_ENUM(ProtocolTypeEnum, name="protocol_type_enum"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    protocol_text: Mapped[str] = mapped_column(String, nullable=False)
    metadata_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Relationships
    institution: Mapped["InstitutionORM"] = relationship(
        "InstitutionORM", 
        back_populates="protocols", 
        passive_deletes=True
    )
    speeches: Mapped[List["SpeechORM"]] = relationship(
        "SpeechORM",
        back_populates="protocol",
    )

    __table_args__ = (
        Index("idx_protocol_institution", "institution_id"),
        Index("idx_protocol_date", "date"),
        Index("idx_protocol_institution_date", "institution_id", "date"),
    )
