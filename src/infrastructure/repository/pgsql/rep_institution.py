from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from src.domain.irepository.context.i_institution import IInstitutionRepository
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.infrastructure.orm.context.orm_institution import InstitutionORM
from src.infrastructure.mappers.context.m_institution import InstitutionMapper


class InstitutionRepository(IInstitutionRepository):
    """PostgreSQL implementation of the Institution repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get_by_id(self, id: UUID) -> Optional[Institution]:
        """Get Institution with all its periods."""
        try:
            orm_institution = self._session.query(InstitutionORM).filter(
                InstitutionORM.id == id.value
            ).one()
            
            return InstitutionMapper.to_domain(orm_institution)
        except NoResultFound:
            return None
    
    def get_by_id_with_periods(self, id: UUID, include_periods: bool = True) -> Optional[Institution]:
        """Get Institution - periods are always included as part of the aggregate."""
        return self.get_by_id(id)
    
    def get_by_country_and_type(self, country_id: UUID, institution_type: InstitutionTypeEnum) -> List[Institution]:
        """Get institutions by country and type."""
        orm_institutions = self._session.query(InstitutionORM).filter(
            InstitutionORM.country_id == country_id.value,
            InstitutionORM.institution_type == institution_type
        ).all()
        
        return [InstitutionMapper.to_domain(orm_inst) for orm_inst in orm_institutions]
    
    def list(self) -> List[Institution]:
        """List all institutions."""
        orm_institutions = self._session.query(InstitutionORM).order_by(
            InstitutionORM.country_id, InstitutionORM.institution_type
        ).all()
        
        return [InstitutionMapper.to_domain(orm_inst) for orm_inst in orm_institutions]
    
    def add(self, institution: Institution) -> None:
        """Add a new institution aggregate."""
        orm_institution = InstitutionMapper.to_orm(institution)
        self._session.add(orm_institution)
        self._session.flush()
    
    def update(self, institution: Institution) -> None:
        """Update an institution aggregate."""
        orm_institution = self._session.query(InstitutionORM).filter(
            InstitutionORM.id == institution.id.value
        ).one()
        
        # Update all fields using mapper
        updated_orm = InstitutionMapper.to_orm(institution)
        orm_institution.institution_type = updated_orm.institution_type
        orm_institution.periods_data = updated_orm.periods_data
        orm_institution.metadata_data = updated_orm.metadata_data
        
        self._session.flush()
    
    def delete(self, id: UUID) -> None:
        """Delete an institution aggregate."""
        orm_institution = self._session.query(InstitutionORM).filter(
            InstitutionORM.id == id.value
        ).one()
        
        self._session.delete(orm_institution)
        self._session.flush()