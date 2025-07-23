from typing import Optional

from src.domain.irepository.text.i_text_raw import IRawTextRepository
from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_raw import RawText
from src.infrastructure.mappers.text.m_text_raw import RawTextMapper
from src.infrastructure.orm.orm_session import session_scope
from src.infrastructure.orm.text.orm_text_raw import RawTextORM


class RawTextRepository(IRawTextRepository):
    def get_by_id(self, id: UUID) -> Optional[RawText]:
        with session_scope() as session:
            orm_raw = session.query(RawTextORM).filter_by(id=id.value).one_or_none()
            if orm_raw:
                return RawTextMapper.to_domain(orm_raw)
            return None

    def get_by_speech_id(self, speech_id: UUID) -> Optional[RawText]:
        with session_scope() as session:
            from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM

            speech_text = session.query(SpeechTextORM).filter_by(speech_id=speech_id.value).one_or_none()
            if not speech_text:
                return None
            orm_raw = session.query(RawTextORM).filter_by(speech_text_id=speech_text.id).one_or_none()
            if orm_raw:
                return RawTextMapper.to_domain(orm_raw)
            return None

    def add(self, raw_text: RawText) -> None:
        with session_scope() as session:
            orm_raw = RawTextMapper.to_orm(raw_text)
            session.add(orm_raw)

    def update(self, raw_text: RawText) -> None:
        with session_scope() as session:
            exists = session.query(RawTextORM).filter_by(id=raw_text.id.value).one_or_none()
            if not exists:
                raise ValueError(f"RawText with id {raw_text.id} not found.")
            orm_raw = RawTextMapper.to_orm(raw_text)
            session.merge(orm_raw)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_raw = session.query(RawTextORM).filter_by(id=id.value).one_or_none()
            if orm_raw:
                session.delete(orm_raw)
