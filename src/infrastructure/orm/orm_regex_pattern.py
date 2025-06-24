from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, String, Boolean, Integer, Text, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.orm_country import CountryORM
    from src.infrastructure.orm.orm_institution import InstitutionORM
    from src.infrastructure.orm.orm_period import PeriodORM
    from src.infrastructure.orm.orm_protocol import ProtocolORM

class RegexPatternORM(Base):
    __tablename__ = "regex_patterns"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    institution_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    period_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("periods.id", ondelete="SET NULL"), nullable=True)
    pattern: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relationships
    country: Mapped["CountryORM"] = relationship(
        "CountryORM"
    )
    institution: Mapped["InstitutionORM"] = relationship(
        "InstitutionORM"
    )
    period: Mapped[Optional["PeriodORM"]] = relationship(
        "PeriodORM"
    )
    protocols: Mapped[List["ProtocolORM"]] = relationship(
        "ProtocolORM",
        back_populates="regex_pattern"
    )

    __table_args__ = (
        UniqueConstraint('country_id', 'institution_id', 'period_id', 'version', 
                        name='uq_regex_pattern_scope_version'),
        Index('idx_regex_country_institution', 'country_id', 'institution_id'),
        Index('idx_regex_active', 'is_active'),
        Index('idx_regex_version', 'version'),
    )
    