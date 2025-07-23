from typing import List, Optional

from src.domain.irepository.context.i_speaker import ISpeakerRepository
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.v_name import Name
from src.infrastructure.mappers.context.m_speaker import SpeakerMapper
from src.infrastructure.orm.context.orm_speaker import SpeakerORM
from src.infrastructure.orm.orm_session import session_scope


class SpeakerRepository(ISpeakerRepository):
    def get_by_id(self, id: UUID) -> Optional[Speaker]:
        with session_scope() as session:
            orm_speaker = session.query(SpeakerORM).filter_by(id=id.value).one_or_none()
            if orm_speaker:
                return SpeakerMapper.to_domain(orm_speaker)
            return None

    def get_by_name(self, name: Name) -> List[Speaker]:
        with session_scope() as session:
            orm_speakers = session.query(SpeakerORM).filter_by(name=str(name)).all()
            return [SpeakerMapper.to_domain(orm) for orm in orm_speakers]

    def list(self) -> List[Speaker]:
        with session_scope() as session:
            orm_speakers = session.query(SpeakerORM).all()
            return [SpeakerMapper.to_domain(orm) for orm in orm_speakers]

    def add(self, speaker: Speaker) -> None:
        with session_scope() as session:
            orm_speaker = SpeakerMapper.to_orm(speaker)
            session.add(orm_speaker)

    def update(self, speaker: Speaker) -> None:
        with session_scope() as session:
            exists = session.query(SpeakerORM).filter_by(id=speaker.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Speaker with id {speaker.id} not found.")
            orm_speaker = SpeakerMapper.to_orm(speaker)
            session.merge(orm_speaker)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_speaker = session.query(SpeakerORM).filter_by(id=id.value).one_or_none()
            if orm_speaker:
                session.delete(orm_speaker)

    def get_by_country_id_and_name(self, country_id: UUID, name: Name) -> Optional[Speaker]:
        with session_scope() as session:
            orm_speaker = (
                session.query(SpeakerORM)
                .filter_by(country_id=country_id.value, name=name.value)
                .one_or_none()
            )
            if orm_speaker:
                return SpeakerMapper.to_domain(orm_speaker)
            return None

    def exists(self, country: CountryEnum, name: Name) -> bool:
        with session_scope() as session:
            orm_speaker = (
                session.query(SpeakerORM).filter_by(country=country.value, name=name.value).one_or_none()
            )
            return orm_speaker is not None
