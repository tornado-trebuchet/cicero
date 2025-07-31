from typing import List, Optional

from backend.domain.irepository.context.i_country import ICountryRepository
from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import CountryEnum
from backend.domain.models.context.a_country import Country
from backend.infrastructure.mappers.context.m_country import CountryMapper
from backend.infrastructure.orm.context.orm_country import CountryORM
from backend.infrastructure.orm.orm_session import session_scope


class CountryRepository(ICountryRepository):
    def get_by_id(self, id: UUID) -> Optional[Country]:
        with session_scope() as session:
            orm_country = session.query(CountryORM).filter_by(id=id.value).one_or_none()
            if orm_country:
                return CountryMapper.to_domain(orm_country)
            return None

    def get_by_country_enum(self, country: CountryEnum) -> Optional[Country]:
        with session_scope() as session:
            orm_country = session.query(CountryORM).filter_by(country=country).one_or_none()
            if orm_country:
                return CountryMapper.to_domain(orm_country)
            return None

    def list(self) -> List[Country]:
        with session_scope() as session:
            orm_countries = session.query(CountryORM).all()
            return [CountryMapper.to_domain(orm) for orm in orm_countries]

    def add(self, country: Country) -> None:
        with session_scope() as session:
            orm_country = CountryMapper.to_orm(country)
            session.add(orm_country)

    def update(self, country: Country) -> None:
        with session_scope() as session:
            exists = session.query(CountryORM).filter_by(id=country.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Country with id {country.id} not found.")
            orm_country = CountryMapper.to_orm(country)
            session.merge(orm_country)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_country = session.query(CountryORM).filter_by(id=id.value).one_or_none()
            if orm_country:
                session.delete(orm_country)

    def exists(self, country: CountryEnum) -> bool:
        with session_scope() as session:
            orm_country = session.query(CountryORM).filter_by(country=country).one_or_none()
            return orm_country is not None
