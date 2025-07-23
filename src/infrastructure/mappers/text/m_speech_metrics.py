from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_speech_metrics_plugin import MetricsPlugin
from src.infrastructure.orm.text.orm_speech_metrics import SpeechMetricsORM


class SpeechMetricsMapper:
    @staticmethod
    def to_orm(domain_entity: MetricsPlugin, speech_id: UUID) -> SpeechMetricsORM:
        orm = SpeechMetricsORM(
            id=domain_entity.id,
            speech_id=speech_id.value,
            dominant_topics=domain_entity.dominant_topics,
            sentiment=domain_entity.sentiment,
            dynamic_codes=domain_entity.dynamic_codes,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: SpeechMetricsORM) -> MetricsPlugin:
        return MetricsPlugin(
            id=UUID(orm_entity.id),
            dominant_topics=orm_entity.dominant_topics,
            sentiment=orm_entity.sentiment,
            dynamic_codes=orm_entity.dynamic_codes,
        )
