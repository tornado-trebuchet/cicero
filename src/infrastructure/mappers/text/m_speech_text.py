from typing import Any, Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.text.v_text_metrics import TextMetrics
from src.infrastructure.orm.text.orm_speech_text import SpeechTextORM


class SpeechTextMapper:
    @staticmethod
    def to_orm(domain_entity: SpeechText) -> SpeechTextORM:
        metrics_data = SpeechTextMapper._metrics_to_orm(domain_entity.text_metrics)
        orm = SpeechTextORM(
            id=domain_entity.id.value,
            speech_id=domain_entity.speech_id.value,
            language_code=domain_entity.language_code,
            metrics=metrics_data,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: SpeechTextORM) -> SpeechText:
        metrics = SpeechTextMapper._metrics_to_domain(orm_entity.metrics)
        return SpeechText(
            id=UUID(orm_entity.id),
            speech_id=UUID(orm_entity.speech_id),
            language_code=orm_entity.language_code,
            raw_text=UUID(orm_entity.raw_text.id),
            clean_text=(UUID(orm_entity.clean_text.id) if orm_entity.clean_text else None),
            translated_text=(UUID(orm_entity.translated_text.id) if orm_entity.translated_text else None),
            sentences=(UUID(orm_entity.sentences.id) if orm_entity.sentences else None),
            tokens=UUID(orm_entity.tokens.id) if orm_entity.tokens else None,
            ngram_tokens=(UUID(orm_entity.ngram_tokens.id) if orm_entity.ngram_tokens else None),
            text_metrics=metrics,
        )

    @staticmethod
    def _metrics_to_orm(
        metrics: Optional[TextMetrics],
    ) -> Optional[dict[str, Any]]:
        if metrics:
            return {
                "word_count": metrics.word_count,
                "character_count": metrics.character_count,
                "token_count": metrics.token_count,
                "unique_token_count": metrics.unique_token_count,
                "sentence_count": metrics.sentence_count,
            }
        return None

    @staticmethod
    def _metrics_to_domain(
        metrics_data: Optional[dict[str, Any]],
    ) -> Optional[TextMetrics]:
        if metrics_data:
            tm = TextMetrics()
            tm.word_count = metrics_data.get("word_count")
            tm.character_count = metrics_data.get("character_count")
            tm.token_count = metrics_data.get("token_count")
            tm.unique_token_count = metrics_data.get("unique_token_count")
            tm.sentence_count = metrics_data.get("sentence_count")
            return tm
        return None
