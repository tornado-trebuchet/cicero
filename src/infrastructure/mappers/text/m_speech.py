from typing import Any, Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.domain.models.text.a_speech import Speech
from src.infrastructure.orm.text.orm_speech import SpeechORM


class SpeechMapper:
    @staticmethod
    def to_orm(domain_entity: Speech) -> SpeechORM:
        meta_data = SpeechMapper._metadata_to_orm(domain_entity.metadata)
        orm = SpeechORM(
            id=domain_entity.id.value,
            protocol_id=domain_entity.protocol_id.value,
            speaker_id=domain_entity.speaker_id.value,
            protocol_order=domain_entity.protocol_order,
            meta_data=meta_data,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: SpeechORM) -> Speech:
        # Metrics will be handled separately through SpeechMetricsRepository
        metadata = SpeechMapper._metadata_to_domain(orm_entity.meta_data)
        return Speech(
            id=UUID(orm_entity.id),
            protocol_id=UUID(orm_entity.protocol_id),
            speaker_id=UUID(orm_entity.speaker_id),
            text=UUID(orm_entity.speech_text.id),
            protocol_order=orm_entity.protocol_order,
            metrics=None,  # To be populated separately by service layer
            metadata=metadata,
        )

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
