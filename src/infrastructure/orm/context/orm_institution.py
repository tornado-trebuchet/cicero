from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict, Any
from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
from src.domain.models.common.v_enums import InstitutionTypeEnum
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.context.orm_country import CountryORM
    from infrastructure.orm.text.orm_protocol import ProtocolORM

class InstitutionORM(Base):
    __tablename__ = "institutions"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    country_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False)
    institution_type: Mapped[InstitutionTypeEnum] = mapped_column(PG_ENUM(InstitutionTypeEnum, name="institution_type_enum"), nullable=False)
    periods_data: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    metadata_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default={})
    
    # Relationships
    country: Mapped["CountryORM"] = relationship(
        "CountryORM", 
        back_populates="institutions"
    )
    protocols: Mapped[List["ProtocolORM"]] = relationship(
        "ProtocolORM",
        back_populates="institution",
    )

    __table_args__ = (
        Index('idx_institution_country', 'country_id'),
        Index('idx_institution_type', 'institution_type'),
        Index('idx_institution_country_type', 'country_id', 'institution_type'),
    )



