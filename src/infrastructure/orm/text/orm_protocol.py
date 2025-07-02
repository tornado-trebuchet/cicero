from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
from src.domain.models.common.v_enums import ProtocolTypeEnum
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_institution import InstitutionORM
    from src.infrastructure.orm.context.orm_period import PeriodORM
    from src.infrastructure.orm.text.orm_speech import SpeechORM

class ProtocolORM(Base):
    __tablename__ = "protocols"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    period_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("periods.id", ondelete="SET NULL"), nullable=True)
    file_source: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    protocol_type: Mapped[ProtocolTypeEnum] = mapped_column(PG_ENUM(ProtocolTypeEnum, name="protocol_type_enum"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    metadata_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default={})
    
    # Relationships
    institution: Mapped["InstitutionORM"] = relationship(
        "InstitutionORM", 
        back_populates="protocols"
    )
    period: Mapped[Optional["PeriodORM"]] = relationship(
        "PeriodORM", 
        back_populates="protocols"
    )
    speeches: Mapped[List["SpeechORM"]] = relationship(
        "SpeechORM",
        back_populates="protocol",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_protocol_institution', 'institution_id'),
        Index('idx_protocol_period', 'period_id'),
        Index('idx_protocol_date', 'date'),
        Index('idx_protocol_type', 'protocol_type'),
        Index('idx_protocol_institution_date', 'institution_id', 'date'),
    )

