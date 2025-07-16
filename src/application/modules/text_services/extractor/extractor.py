from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
from src.application.modules.text_services.extractor.extractor_spec import ExtractionSpec
from src.domain.services.text.extractor.serv_extractor import ExtractSpeakersFromProtocol
from src.domain.models.common.v_common import UUID
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.services.text.extractor.serv_extractor_dto import SpeechDTO

class ExtractorService:
    def __init__(self):
        self.protocol_repo = ProtocolRepository()
        self.speech_repo = SpeechRepository()

    def extract_speeches(self, protocol_id: UUID, spec: ExtractionSpec):
        protocol = self.protocol_repo.get_by_id(protocol_id)
        if not protocol:
            raise ValueError(f"Protocol with id {protocol_id} not found.")
        extractor = ExtractSpeakersFromProtocol(protocol, spec)
        pattern_cls = extractor.pick_pattern()
        if not pattern_cls:
            raise ValueError("No matching regex pattern found for provided spec.")
        speeches_dto = extractor.process(protocol, pattern_cls)
        # Persist speeches, avoid duplicates
        for speech_dto in speeches_dto:
            # Convert DTO to domain model
            speech_id = UUID("00000000-0000-0000-0000-000000000000")  # Placeholder
            raw_text_id = UUID("00000000-0000-0000-0000-000000000001")  # Placeholder
            speaker_id = UUID("00000000-0000-0000-0000-000000000002")  # Placeholder
            speech_text = SpeechText(
                id=raw_text_id,
                speech_id=speech_id,
                raw_text=raw_text_id,
                language_code=spec.language,
            )
            speech = Speech(
                id=speech_id,
                protocol_id=protocol_id,
                speaker_id=speaker_id,
                text=speech_text,
                metadata=None,
                metrics=None
            )
            existing = [s for s in self.speech_repo.get_by_protocol_id(protocol_id) if s.speaker_id == speaker_id and s.text.raw_text == raw_text_id]
            if not existing:
                self.speech_repo.add(speech)
        return speeches_dto
