from typing import List
from src.domain.models.text.a_protocol import Protocol
from src.domain.services.text.base_text_service import TextService
from src.domain.services.text.extractor.regex.base_regex import RegexPattern
from src.domain.services.text.extractor.serv_extractor_dto import SpeechDTO, SpeakerDTO, RawTextDTO
from src.application.modules.text_services.extractor.extractor_spec import ExtractionSpec

class ExtractSpeakersFromProtocol(TextService):
    def __init__(self, protocol: Protocol, spec: ExtractionSpec):
        self.protocol = protocol
        self.country = spec.country
        self.institution = spec.institution
        self.language = spec.language
        self.pattern_spec = spec.pattern_spec


    def pick_pattern(self) -> type[RegexPattern] | None:
        pattern_cls = RegexPattern.find_by_specifications(
            country_code=self.country,
            institution_code=self.institution,
            language_code=self.language,
            protocol_type=self.protocol.protocol_type
        )
        return pattern_cls

    def process(self, protocol: Protocol, pattern_cls: type[RegexPattern]) -> List[SpeechDTO]:
        text = protocol.protocol_text.protocol_text
        pattern_instance = pattern_cls()
        regex = pattern_instance.compile_pattern()
        matches = regex.findall(text)
        speeches: List[SpeechDTO] = []
        for match in matches:
            speaker_name = match[0]
            speech_text = match[1]
            speaker_dto = SpeakerDTO(name=speaker_name)
            raw_text_dto = RawTextDTO(text=speech_text)
            speech_dto = SpeechDTO(
                speaker=speaker_dto,
                raw_text=raw_text_dto,
                language_code=self.language,
                metadata=None,
                metrics=None
            )
            speeches.append(speech_dto)
        return speeches
