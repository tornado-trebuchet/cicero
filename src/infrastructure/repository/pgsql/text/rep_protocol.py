from src.domain.irepository.text.i_protocol import IProtocolRepository
from src.domain.models.text.a_protocol import Protocol
from src.domain.models.common.v_common import UUID, DateTime, HttpUrl
from src.infrastructure.orm.text.orm_protocol import ProtocolORM
from src.infrastructure.mappers.text.m_protocol import ProtocolMapper
from src.infrastructure.orm.orm_session import session_scope
from typing import Optional, List

class ProtocolRepository(IProtocolRepository):
    def get_by_id(self, id: UUID) -> Optional[Protocol]:
        with session_scope() as session:
            orm_protocol = session.query(ProtocolORM).filter_by(id=id.value).one_or_none()
            if orm_protocol:
                return ProtocolMapper.to_domain(orm_protocol)
            return None

    def get_by_country_id(self, country_id: UUID) -> List[Protocol]:
        with session_scope() as session:
            orm_protocols = session.query(ProtocolORM).join(ProtocolORM.institution).filter_by(country_id=country_id.value).all()
            return [ProtocolMapper.to_domain(orm) for orm in orm_protocols]

    def get_by_institution_id(self, institution_id: UUID) -> List[Protocol]:
        with session_scope() as session:
            orm_protocols = session.query(ProtocolORM).filter_by(institution_id=institution_id.value).all()
            return [ProtocolMapper.to_domain(orm) for orm in orm_protocols]

    def get_by_institution_and_period(self, institution_id: UUID, period_id: UUID) -> List[Protocol]:
        with session_scope() as session:
            orm_protocols = session.query(ProtocolORM).filter_by(institution_id=institution_id.value, period_id=period_id.value).all()
            return [ProtocolMapper.to_domain(orm) for orm in orm_protocols]

    def get_by_date_range(self, start_date: DateTime, end_date: DateTime) -> List[Protocol]:
        with session_scope() as session:
            orm_protocols = session.query(ProtocolORM).filter(ProtocolORM.date >= start_date, ProtocolORM.date <= end_date).all()
            return [ProtocolMapper.to_domain(orm) for orm in orm_protocols]

    def list(self) -> List[Protocol]:
        with session_scope() as session:
            orm_protocols = session.query(ProtocolORM).all()
            return [ProtocolMapper.to_domain(orm) for orm in orm_protocols]

    def add(self, protocol: Protocol) -> None:
        with session_scope() as session:
            orm_protocol = ProtocolMapper.to_orm(protocol)
            session.add(orm_protocol)

    def update(self, protocol: Protocol) -> None:
        with session_scope() as session:
            exists = session.query(ProtocolORM).filter_by(id=protocol.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Protocol with id {protocol.id} not found.")
            orm_protocol = ProtocolMapper.to_orm(protocol)
            session.merge(orm_protocol)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_protocol = session.query(ProtocolORM).filter_by(id=id.value).one_or_none()
            if orm_protocol:
                session.delete(orm_protocol)

    def get_speeches_by_protocol_id(self, protocol_id: UUID) -> List[UUID]:
        with session_scope() as session:
            orm_protocol = session.query(ProtocolORM).filter_by(id=protocol_id.value).one_or_none()
            if orm_protocol and hasattr(orm_protocol, 'speeches'):
                return [UUID(s.id) for s in orm_protocol.speeches]
            return []

    def get_by_date(self, date: DateTime) -> List[Protocol]:
        with session_scope() as session:
            orm_protocols = session.query(ProtocolORM).filter_by(date=date).all()
            return [ProtocolMapper.to_domain(orm) for orm in orm_protocols]

    def get_by_source(self, source: HttpUrl) -> List[Protocol]:
        with session_scope() as session:
            orm_protocols = session.query(ProtocolORM).filter_by(file_source=str(source)).all()
            return [ProtocolMapper.to_domain(orm) for orm in orm_protocols]

    def exists(self, source: HttpUrl) -> bool:
        with session_scope() as session:
            orm_protocol = session.query(ProtocolORM).filter_by(file_source=str(source)).one_or_none()
            return orm_protocol is not None