from src.domain.models.text.a_speech import Speech
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.text.e_speech_text import Text
from src.domain.models.common.v_common import UUID
from src.domain.models.text.v_speech_metrics_plugin import MetricsPlugin
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.infrastructure.orm.text.orm_speech import SpeechORM


class SpeechMapper:
    
    @staticmethod
    def to_orm(domain_entity: Speech) -> SpeechORM:
        metrics_data = None
        if domain_entity.metrics:
            metrics_data = {
                "dominant_topics": domain_entity.metrics.dominant_topics,
                "sentiment": domain_entity.metrics.sentiment,
                "dynamic_codes": domain_entity.metrics.dynamic_codes
            }
        
        return SpeechORM(
            id=domain_entity.id.value,
            protocol_id=domain_entity.protocol_id.value,
            author_id=domain_entity.speaker.id.value, 
            metrics_data=metrics_data,
            metadata_data=domain_entity.metadata._data if domain_entity.metadata else {}
        )
    
    @staticmethod
    def to_domain(orm_entity: SpeechORM, speaker: Speaker, text: Text) -> Speech:

        metrics = None
        metrics_data = getattr(orm_entity, 'metrics_data', None)
        if metrics_data:
            metrics = MetricsPlugin(
                dominant_topics=metrics_data.get("dominant_topics", []),
                sentiment=metrics_data.get("sentiment", {}),
                dynamic_codes=metrics_data.get("dynamic_codes", [])
            )
        
        metadata_data = getattr(orm_entity, 'metadata_data', {}) or {}
        
        return Speech(
            id=UUID(str(orm_entity.id)),
            protocol_id=UUID(str(orm_entity.protocol_id)),
            speaker=speaker,
            text=text,
            metrics=metrics,
            metadata=MetadataPlugin(metadata_data)
        )