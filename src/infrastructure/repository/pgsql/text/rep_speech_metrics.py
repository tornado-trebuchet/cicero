from typing import Optional

from src.domain.irepository.text.i_speech_metrics import ISpeechMetricsRepository
from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_speech_metrics_plugin import MetricsPlugin
from src.infrastructure.mappers.text.m_speech_metrics import SpeechMetricsMapper
from src.infrastructure.orm.orm_session import session_scope
from src.infrastructure.orm.text.orm_speech_metrics import SpeechMetricsORM


class SpeechMetricsRepository(ISpeechMetricsRepository):
    def get_by_speech_id(self, speech_id: UUID) -> Optional[MetricsPlugin]:
        with session_scope() as session:
            orm_metrics = session.query(SpeechMetricsORM).filter_by(speech_id=speech_id.value).one_or_none()
            if orm_metrics:
                return SpeechMetricsMapper.to_domain(orm_metrics)
            return None

    def add(self, speech_id: UUID, metrics: MetricsPlugin) -> None:
        with session_scope() as session:
            orm_metrics = SpeechMetricsMapper.to_orm(metrics, speech_id)
            session.add(orm_metrics)

    def update(self, speech_id: UUID, metrics: MetricsPlugin) -> None:
        with session_scope() as session:
            existing = session.query(SpeechMetricsORM).filter_by(speech_id=speech_id.value).one_or_none()
            if not existing:
                raise ValueError(f"SpeechMetrics for speech {speech_id} not found.")

            # Update existing record
            existing.dominant_topics = metrics.dominant_topics
            existing.sentiment = metrics.sentiment
            existing.dynamic_codes = metrics.dynamic_codes

    def delete(self, speech_id: UUID) -> None:
        with session_scope() as session:
            orm_metrics = session.query(SpeechMetricsORM).filter_by(speech_id=speech_id.value).one_or_none()
            if orm_metrics:
                session.delete(orm_metrics)
