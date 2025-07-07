from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.text.v_text_metrics import TextMetrics
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import LanguageEnum
from src.infrastructure.orm.text.orm_speech_text import TextORM

class SpeechTextMapper:
    @staticmethod
    def to_orm(domain_entity: SpeechText) -> TextORM:
        metrics_data = SpeechTextMapper._metrics_to_orm(domain_entity.text_metrics)
        orm = TextORM(
            id=domain_entity.id.value,
            speech_id=domain_entity.speech_id.value,
            raw_text_id=domain_entity.raw_text.value,
            language_code=domain_entity.language_code,
            clean_text_id=domain_entity.clean_text.value if domain_entity.clean_text else None,
            translated_text_id=domain_entity.translated_text.value if domain_entity.translated_text else None,
            sentences_id=domain_entity.sentences.value if domain_entity.sentences else None,
            tokens_id=domain_entity.tokens.value if domain_entity.tokens else None,
            ngram_tokens_id=domain_entity.ngram_tokens.value if domain_entity.ngram_tokens else None,
            metrics=metrics_data
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: TextORM) -> SpeechText:
        metrics = SpeechTextMapper._metrics_to_domain(orm_entity.metrics)
        return SpeechText(
            id=UUID(orm_entity.id),
            speech_id=UUID(orm_entity.speech_id),
            raw_text=UUID(orm_entity.raw_text_id),
            language_code=orm_entity.language_code,
            clean_text=UUID(orm_entity.clean_text_id) if orm_entity.clean_text_id else None,
            translated_text=UUID(orm_entity.translated_text_id) if orm_entity.translated_text_id else None,
            sentences=UUID(orm_entity.sentences_id) if orm_entity.sentences_id else None,
            tokens=UUID(orm_entity.tokens_id) if orm_entity.tokens_id else None,
            ngram_tokens=UUID(orm_entity.ngram_tokens_id) if orm_entity.ngram_tokens_id else None,
            text_metrics=metrics
        )

    @staticmethod
    def _metrics_to_orm(metrics: TextMetrics | None):
        if metrics:
            return {
                'word_count': metrics.word_count,
                'character_count': metrics.character_count,
                'token_count': metrics.token_count,
                'unique_token_count': metrics.unique_token_count,
                'sentence_count': metrics.sentence_count
            }
        return None

    @staticmethod
    def _metrics_to_domain(metrics_data):
        if metrics_data:
            tm = TextMetrics()
            tm.word_count = metrics_data.get('word_count')
            tm.character_count = metrics_data.get('character_count')
            tm.token_count = metrics_data.get('token_count')
            tm.unique_token_count = metrics_data.get('unique_token_count')
            tm.sentence_count = metrics_data.get('sentence_count')
            return tm
        return None
