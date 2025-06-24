from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.orm.base_orm import Base
from src.domain.models.v_enums import CountryEnum
import uuid

if TYPE_CHECKING:
    from src.infrastructure.orm.orm_institution import InstitutionORM

class CountryORM(Base):
    __tablename__ = "countries"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[CountryEnum] = mapped_column(PG_ENUM(CountryEnum, name="country_enum"), nullable=False, unique=True)
    
    # Relationships
    institutions: Mapped[List["InstitutionORM"]] = relationship(
        "InstitutionORM", 
        back_populates="country",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_country_name', 'name'),
    )
    