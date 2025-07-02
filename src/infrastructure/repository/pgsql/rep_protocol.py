from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from domain.irepository.text.i_protocol import IProtocolRepository
from src.domain.models.text.a_protocol import Protocol
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
        self._session.flush()  # Ensure ID is generate
    
    def update(self, protocol: Protocol) -> None:
        """Update an existing protocol."""
        orm_protocol = self._session.query(ProtocolORM).filter(
            ProtocolORM.id == protocol.id.value
        ).one()
        
        # Update fields from domain entity
        updated_orm = ProtocolMapper.to_orm(protocol)
        orm_protocol.institution_id = updated_orm.institution_id
        orm_protocol.period_id = updated_orm.period_id
        orm_protocol.file_source = updated_orm.file_source
        orm_protocol.protocol_type = updated_orm.protocol_type
        orm_protocol.date = updated_orm.date
        orm_protocol.metadata_data = updated_orm.metadata_data
        
        self._session.flush()
    
    def delete(self, id: UUID) -> None:
        """Delete a protocol (will cascade delete speeches)."""
        orm_protocol = self._session.query(ProtocolORM).filter(
            ProtocolORM.id == id.value
        ).one()
        
        self._session.delete(orm_protocol)
        self._session.flush()