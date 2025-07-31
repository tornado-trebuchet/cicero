from typing import List, Optional

from backend.domain.irepository.context.i_institution import IInstitutionRepository
from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import InstitutionTypeEnum
from backend.domain.models.context.e_institution import Institution
from backend.domain.models.context.v_label import Label
from backend.infrastructure.mappers.context.m_institution import InstitutionMapper
from backend.infrastructure.orm.context.orm_institution import InstitutionORM
from backend.infrastructure.orm.orm_session import session_scope


class InstitutionRepository(IInstitutionRepository):
    def get_by_id(self, id: UUID) -> Optional[Institution]:
        with session_scope() as session:
            orm_institution = session.query(InstitutionORM).filter_by(id=id.value).one_or_none()
            if orm_institution:
                return InstitutionMapper.to_domain(orm_institution)
            return None

    def get_by_type(self, institution_type: InstitutionTypeEnum) -> List[Institution]:
        with session_scope() as session:
            orm_institutions = (
                session.query(InstitutionORM).filter_by(institution_type=institution_type).all()
            )
            return [InstitutionMapper.to_domain(orm) for orm in orm_institutions]

    def get_by_label(self, label: Label) -> Optional[Institution]:
        with session_scope() as session:
            orm_institution = session.query(InstitutionORM).filter_by(label=label).one_or_none()
            if orm_institution:
                return InstitutionMapper.to_domain(orm_institution)
            return None

    def get_by_country_id_and_type(
        self, country_id: UUID, institution_type: InstitutionTypeEnum
    ) -> Optional[Institution]:
        with session_scope() as session:
            orm_institution = (
                session.query(InstitutionORM)
                .filter_by(
                    country_id=country_id.value,
                    institution_type=institution_type,
                )
                .one_or_none()
            )
            if orm_institution:
                return InstitutionMapper.to_domain(orm_institution)
            return None

    def list(self) -> List[Institution]:
        with session_scope() as session:
            orm_institutions = session.query(InstitutionORM).all()
            return [InstitutionMapper.to_domain(orm) for orm in orm_institutions]

    def list_by_country_id(self, country_id: UUID) -> List[Institution]:
        with session_scope() as session:
            orm_institutions = session.query(InstitutionORM).filter_by(country_id=country_id.value).all()
            return [InstitutionMapper.to_domain(orm) for orm in orm_institutions]

    def add(self, institution: Institution) -> None:
        with session_scope() as session:
            orm_institution = InstitutionMapper.to_orm(institution)
            session.add(orm_institution)

    def update(self, institution: Institution) -> None:
        with session_scope() as session:
            exists = session.query(InstitutionORM).filter_by(id=institution.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Institution with id {institution.id} not found.")
            orm_institution = InstitutionMapper.to_orm(institution)
            session.merge(orm_institution)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_institution = session.query(InstitutionORM).filter_by(id=id.value).one_or_none()
            if orm_institution:
                session.delete(orm_institution)

    def exists(self, country_id: UUID, institution_type: InstitutionTypeEnum) -> bool:
        with session_scope() as session:
            orm_institution = (
                session.query(InstitutionORM)
                .filter_by(
                    country_id=country_id.value,
                    institution_type=institution_type,
                )
                .one_or_none()
            )
            return orm_institution is not None
