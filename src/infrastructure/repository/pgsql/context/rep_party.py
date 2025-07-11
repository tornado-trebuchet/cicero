from src.domain.irepository.context.i_party import IPartyRepository
from src.domain.models.context.e_party import Party
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_party_name import PartyName
from src.infrastructure.orm.context.orm_party import PartyORM
from src.infrastructure.mappers.context.m_party import PartyMapper
from src.infrastructure.orm.orm_session import session_scope
from typing import Optional, List

class PartyRepository(IPartyRepository):
    def get_by_id(self, id: UUID) -> Optional[Party]:
        with session_scope() as session:
            orm_party = session.query(PartyORM).filter_by(id=id.value).one_or_none()
            if orm_party:
                return PartyMapper.to_domain(orm_party)
            return None

    def get_by_name(self, party_name: PartyName) -> Optional[Party]:
        with session_scope() as session:
            orm_party = session.query(PartyORM).filter_by(party_name=str(party_name)).one_or_none()
            if orm_party:
                return PartyMapper.to_domain(orm_party)
            return None

    def list(self) -> List[Party]:
        with session_scope() as session:
            orm_parties = session.query(PartyORM).all()
            return [PartyMapper.to_domain(orm) for orm in orm_parties]

    def add(self, party: Party) -> None:
        with session_scope() as session:
            orm_party = PartyMapper.to_orm(party)
            session.add(orm_party)

    def update(self, party: Party) -> None:
        with session_scope() as session:
            exists = session.query(PartyORM).filter_by(id=party.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Party with id {party.id} not found.")
            orm_party = PartyMapper.to_orm(party)
            session.merge(orm_party)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_party = session.query(PartyORM).filter_by(id=id.value).one_or_none()
            if orm_party:
                session.delete(orm_party)