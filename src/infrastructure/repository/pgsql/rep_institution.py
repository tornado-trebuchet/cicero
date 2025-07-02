from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from domain.irepository.context.i_institution import IInstitutionRepository
from domain.models.context.e_institution import Institution
from src.domain.models.context.v_period import Period
from domain.models.common.v_common import UUID
from domain.models.common.v_enums import InstitutionTypeEnum
from infrastructure.orm.context.orm_institution import InstitutionORM
from infrastructure.orm.context.orm_period import PeriodORM
from infrastructure.orm.text.orm_protocol import ProtocolORM
from infrastructure.mappers.context.m_institution import InstitutionMapper
from infrastructure.mappers.context.m_period import PeriodMapper


class InstitutionRepository(IInstitutionRepository):
    """PostgreSQL implementation of the Institution repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Institution]:
        """Get fully rehydrated Institution with all its periods."""
        return self.get_by_id_with_periods(id, include_periods=True)
    
    def get_by_id_with_periods(self, id: UUID, include_periods: bool = True) -> Optional[Institution]:
        """Get Institution with optional period loading for performance."""
        try:
            orm_institution = self._session.query(InstitutionORM).filter(
                InstitutionORM.id == id.value
            ).one()
            
            institution = InstitutionMapper.to_domain(orm_institution)
            
            if include_periods:
                # Load periods that are referenced by protocols of this institution
                periods_query = self._session.query(PeriodORM).join(
                    ProtocolORM, PeriodORM.id == ProtocolORM.period_id
                ).filter(
                    ProtocolORM.institution_id == id.value
                ).distinct()
                
                periods = [PeriodMapper.to_domain(p) for p in periods_query]
                institution.periodisation = periods
            
            return institution
        except NoResultFound:
            return None
    
    def get_by_country_and_type(self, country_id: UUID, institution_type: InstitutionTypeEnum) -> List[Institution]:
        """Get institutions by country and type with periods."""
        orm_institutions = self._session.query(InstitutionORM).filter(
            InstitutionORM.country_id == country_id.value,
            InstitutionORM.institution_type == institution_type
        ).all()
        
        institutions = []
        for orm_inst in orm_institutions:
            institution = InstitutionMapper.to_domain(orm_inst)
            
            # Load periods for each institution
            periods_query = self._session.query(PeriodORM).join(
                ProtocolORM, PeriodORM.id == ProtocolORM.period_id
            ).filter(
                ProtocolORM.institution_id == orm_inst.id
            ).distinct()
            
            institution.periodisation = [PeriodMapper.to_domain(p) for p in periods_query]
            institutions.append(institution)
        
        return institutions
    
    def list(self) -> List[Institution]:
        """List all institutions with their periods."""
        orm_institutions = self._session.query(InstitutionORM).order_by(
            InstitutionORM.country_id, InstitutionORM.institution_type
        ).all()
        
        institutions = []
        for orm_inst in orm_institutions:
            institution = InstitutionMapper.to_domain(orm_inst)
            
            # Load periods for each institution
            periods_query = self._session.query(PeriodORM).join(
                ProtocolORM, PeriodORM.id == ProtocolORM.period_id
            ).filter(
                ProtocolORM.institution_id == orm_inst.id
            ).distinct()
            
            institution.periodisation = [PeriodMapper.to_domain(p) for p in periods_query]
            institutions.append(institution)
        
        return institutions
    
    def add(self, institution: Institution) -> None:
        """
        Add a new institution aggregate.
        Will persist Institution and all its Period entities as a transaction.
        """
        # Add the institution
        orm_institution = InstitutionMapper.to_orm(institution)
        self._session.add(orm_institution)
        self._session.flush()  # Ensure institution ID is available
        
        # Add periods
        for period in institution.periodisation or []:
            orm_period = PeriodMapper.to_orm(period)
            self._session.add(orm_period)
        
        self._session.flush()
    
    def update(self, institution: Institution) -> None:
        """
        Update an institution aggregate.
        Will update Institution and sync its Period entities.
        """
        # Update institution
        orm_institution = self._session.query(InstitutionORM).filter(
            InstitutionORM.id == institution.id.value
        ).one()
        
        # Update basic fields
        orm_institution.institution_type = institution.institution_type
        orm_institution.metadata_data = institution.metadata._data if institution.metadata else {}
        
        
        self._session.flush()
    
    def delete(self, id: UUID) -> None:
        """
        Delete an institution aggregate.
        Will cascade delete all contained protocols (periods may remain if used elsewhere).
        """
        orm_institution = self._session.query(InstitutionORM).filter(
            InstitutionORM.id == id.value
        ).one()
        
        self._session.delete(orm_institution)
        self._session.flush()
    
    def add_period_to_institution(self, institution_id: UUID, period: Period) -> None:
        """Add a new period to an existing institution."""
        # Check if institution exists
        institution_exists = self._session.query(InstitutionORM).filter(
            InstitutionORM.id == institution_id.value
        ).first()
        
        if not institution_exists:
            raise ValueError(f"Institution with id {institution_id} not found")
        
        # Add the period if it doesn't exist
        existing_period = self._session.query(PeriodORM).filter(
            PeriodORM.id == period.id.value # FIXME no longer entity
        ).first()
        
        if not existing_period:
            orm_period = PeriodMapper.to_orm(period)
            self._session.add(orm_period)
            self._session.flush()
    
    def remove_period_from_institution(self, institution_id: UUID, period_id: UUID) -> None:
        """Remove a period from an institution."""
        # Check if the period is still referenced by protocols of this institution
        protocol_count = self._session.query(ProtocolORM).filter(
            ProtocolORM.institution_id == institution_id.value,
            ProtocolORM.period_id == period_id.value
        ).count()
        
        if protocol_count > 0:
            raise ValueError(
                f"Cannot remove period {period_id} from institution {institution_id} "
                f"because it's still referenced by {protocol_count} protocol(s)"
            )
        
        pass