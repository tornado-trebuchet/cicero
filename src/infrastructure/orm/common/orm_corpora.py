from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Text, ForeignKey, Table, Index, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM, ARRAY
from src.infrastructure.orm.base_orm import Base
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.text.orm_speech import SpeechORM

# Association table for corpora-speech many-to-many relationship
# TODO: Consider partitioning this table by country or time period for performance
corpora_speeches = Table(
    'corpora_speeches',
    Base.metadata,
    Column('corpora_id', PG_UUID(as_uuid=True), ForeignKey('corpora.id'), primary_key=True),
    Column('speech_id', PG_UUID(as_uuid=True), ForeignKey('speeches.id'), primary_key=True)
)


class CorporaORM(Base):
    """ORM model for Corpora aggregate with memory-efficient speech handling."""
    
    __tablename__ = 'corpora'
    
    # TODO: Add database indexes for performance optimization
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[CountryEnum] = mapped_column(PG_ENUM(CountryEnum, name="country_enum"), nullable=False)
    institution: Mapped[InstitutionTypeEnum] = mapped_column(PG_ENUM(InstitutionTypeEnum, name="institution_enum"), nullable=False)
    
    # Store party as string since PartyEnumRegistry is dynamic
    party: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Store periods as array of strings (serialized Period objects)
    # TODO: Consider separate Period table for better normalization
    periods: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text), nullable=True)
    
    # Lazy-loaded relationship to speeches to prevent memory issues
    # Use lazy='dynamic' to get a query object instead of loading all speeches
    speeches: Mapped[List["SpeechORM"]] = relationship(
        "SpeechORM",
        secondary=corpora_speeches,
        lazy='dynamic',  # Critical for memory efficiency
        back_populates="corpora"
    )
    
    __table_args__ = (
        Index('idx_corpora_country', 'country'),
        Index('idx_corpora_institution', 'institution'),
        Index('idx_corpora_label', 'label'),
    )