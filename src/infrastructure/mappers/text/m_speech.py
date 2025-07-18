from typing import Any, Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.v_speech_metrics_plugin import MetricsPlugin
from src.infrastructure.orm.text.orm_speech import SpeechORM


class SpeechMapper:
    @staticmethod
    def to_orm(domain_entity: Speech) -> SpeechORM:
        metrics_data = SpeechMapper._metrics_to_orm(domain_entity.metrics)
        meta_data = SpeechMapper._metadata_to_orm(domain_entity.metadata)
        orm = SpeechORM(
            id=domain_entity.id.value,
            protocol_id=domain_entity.protocol_id.value,
            speaker_id=domain_entity.speaker_id.value,
            protocol_order=domain_entity.protocol_order,
            metrics_data=metrics_data,
            meta_data=meta_data,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: SpeechORM) -> Speech:
        metrics = SpeechMapper._metrics_to_domain(orm_entity.metrics_data)
        metadata = SpeechMapper._metadata_to_domain(orm_entity.meta_data)
        return Speech(
            id=UUID(orm_entity.id),
            protocol_id=UUID(orm_entity.protocol_id),
            speaker_id=UUID(orm_entity.speaker_id),
            text=UUID(orm_entity.speech_text.id),
            protocol_order=orm_entity.protocol_order,
            metrics=metrics,
            metadata=metadata,
        )

    @staticmethod
    def _metrics_to_orm(
        metrics: Optional[MetricsPlugin],
    ) -> Optional[dict[str, Any]]:
        if metrics:
            return {
                "dominant_topics": metrics.dominant_topics,
                "sentiment": metrics.sentiment,
                "dynamic_codes": metrics.dynamic_codes,
            }
        return None

    @staticmethod
    def _metrics_to_domain(
        metrics_data: Optional[dict[str, Any]],
    ) -> Optional[MetricsPlugin]:
        if metrics_data:
            return MetricsPlugin(
                dominant_topics=metrics_data.get("dominant_topics"),
                sentiment=metrics_data.get("sentiment"),
                dynamic_codes=metrics_data.get("dynamic_codes"),
            )
        return None

    @staticmethod
    def _metadata_to_orm(
        metadata: Optional[MetadataPlugin],
    ) -> Optional[dict[str, Any]]:
        return metadata.get_properties() if metadata else None

    @staticmethod
    def _metadata_to_domain(
        meta_data: Optional[dict[str, Any]],
    ) -> Optional[MetadataPlugin]:
        return MetadataPlugin(meta_data) if meta_data else None
