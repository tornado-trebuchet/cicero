from src.domain.models.text.e_text_raw import RawText
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_text_raw import RawTextORM

class RawTextMapper:
    @staticmethod
    def to_orm(domain_entity: RawText) -> RawTextORM:
        orm = RawTextORM(
            id=domain_entity.id.value,
            speech_text_id=domain_entity.speech_id.value,
            text=domain_entity.text
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: RawTextORM) -> RawText:
        return RawText(
            id=UUID(orm_entity.id),
            speech_id=UUID(orm_entity.speech_text_id),
            text=orm_entity.text
        )
