from src.domain.irepository.common.i_joint_q import IJointQRepository
from src.domain.models.common.v_enums import InstitutionTypeEnum, CountryEnum
from src.domain.models.context.e_institution import Institution
from src.infrastructure.orm.context.orm_institution import InstitutionORM
from src.infrastructure.orm.context.orm_country import CountryORM
from src.infrastructure.mappers.context.m_institution import InstitutionMapper
from src.infrastructure.orm.orm_session import session_scope
from src.infrastructure.mappers.context.m_country import CountryMapper
from src.domain.models.context.a_country import Country
from src.domain.models.common.v_common import UUID

from typing import Optional

class JointQRepository(IJointQRepository):
    def get_institution_by_country_and_institution_enum(self, country: CountryEnum, institution_enum: InstitutionTypeEnum) -> Optional[Institution]:
        with session_scope() as session:
            # Find the country id by enum
            country_orm = session.query(CountryORM).filter_by(country=country).one_or_none()
            if not country_orm:
                return None
            # Find the institution by country_id and institution_type
            orm_institution = session.query(InstitutionORM).filter_by(
                country_id=country_orm.id,
                institution_type=institution_enum
            ).one_or_none()
            if orm_institution:
                return InstitutionMapper.to_domain(orm_institution)
            return None

    def get_country_by_institution_id(self, institution_id: UUID) -> Optional[Country]:
        with session_scope() as session:
            # Find the institution by id
            orm_institution = session.query(InstitutionORM).filter_by(id=institution_id.value).one_or_none()
            if not orm_institution:
                return None
            # Get the country associated with the institution
            orm_country = session.query(CountryORM).filter_by(id=orm_institution.country_id).one_or_none()
            if orm_country:
                return CountryMapper.to_domain(orm_country)
            return None