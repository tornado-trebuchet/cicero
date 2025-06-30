from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from domain.irepository.text.i_protocol import IProtocolRepository
from domain.models.text.e_protocol import Protocol
from domain.models.common.v_common import UUID
from infrastructure.orm.text.orm_protocol import ProtocolORM
from infrastructure.mappers.context.m_protocol import ProtocolMapper


class ProtocolRepository(IProtocolRepository):
    """PostgreSQL implementation of the Protocol repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Protocol]:
        """Get protocol by ID."""
        try:
            orm_protocol = self._session.query(ProtocolORM).filter(
                ProtocolORM.id == id.value
            ).one()
            return ProtocolMapper.to_domain(orm_protocol)
        except NoResultFound:
            return None
    
    def get_by_institution_id(self, institution_id: UUID) -> List[Protocol]:
        """Get all protocols for an institution."""
        orm_protocols = self._session.query(ProtocolORM).filter(
            ProtocolORM.institution_id == institution_id.value
        ).order_by(ProtocolORM.date.desc()).all()
        
        return [ProtocolMapper.to_domain(orm_protocol) for orm_protocol in orm_protocols]
    
    def get_by_institution_and_period(self, institution_id: UUID, period_id: UUID) -> List[Protocol]:
        """Get protocols for a specific institution and period."""
        orm_protocols = self._session.query(ProtocolORM).filter(
            ProtocolORM.institution_id == institution_id.value,
            ProtocolORM.period_id == period_id.value
        ).order_by(ProtocolORM.date.desc()).all()
        
        return [ProtocolMapper.to_domain(orm_protocol) for orm_protocol in orm_protocols]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Protocol]:
        """Get protocols within a date range."""
        orm_protocols = self._session.query(ProtocolORM).filter(
            ProtocolORM.date >= start_date,
            ProtocolORM.date <= end_date
        ).order_by(ProtocolORM.date.desc()).all()
        
        return [ProtocolMapper.to_domain(orm_protocol) for orm_protocol in orm_protocols]
    
    def list(self) -> List[Protocol]:
        """List all protocols."""
        orm_protocols = self._session.query(ProtocolORM).order_by(
            ProtocolORM.date.desc()
        ).all()
        
        return [ProtocolMapper.to_domain(orm_protocol) for orm_protocol in orm_protocols]
    
    def add(self, protocol: Protocol) -> None:
        """Add a new protocol."""
        orm_protocol = ProtocolMapper.to_orm(protocol)
        self._session.add(orm_protocol)
        self._session.flush()  # Ensure ID is generated
    
    def update(self, protocol: Protocol) -> None:
        """Update a protocol in the database using explicit field assignments.
        
        FIXME: This method is error-prone and should be refactored to use explicit helpers for value object unwrapping and type conversions.
        """
        orm_protocol: ProtocolORM = self._session.query(ProtocolORM).filter(
            ProtocolORM.id == protocol.id.value
        ).one()

        # Update fields with explicit unwrapping and type handling
        orm_protocol.institution_id = protocol.institution_id.value  # UUID -> DB UUID
        # FIXME: period may be a value object or None; clarify type and unwrap as needed
        orm_protocol.period_id = protocol.period.id.value if protocol.period else None
        orm_protocol.extension = protocol.extension  # str
        # FIXME: file_source may be a value object; clarify and unwrap as needed
        orm_protocol.file_source = str(protocol.file_source) if protocol.file_source else None
        orm_protocol.protocol_type = protocol.protocol_type  # str or enum
        orm_protocol.date = protocol.date.value  # Date value object -> DB date
        # FIXME: metadata may be a dict, JSON, or value object; clarify and unwrap as needed
        orm_protocol.metadata_data = protocol.metadata

        self._session.flush()
    
    def delete(self, id: UUID) -> None:
        """Delete a protocol (will cascade delete speeches)."""
        orm_protocol = self._session.query(ProtocolORM).filter(
            ProtocolORM.id == id.value
        ).one()
        
        self._session.delete(orm_protocol)
        self._session.flush()