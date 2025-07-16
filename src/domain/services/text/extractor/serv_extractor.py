from typing import List
from src.domain.models.common.v_common import UUID
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.text.e_text_raw import RawText
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_protocol import Protocol
from src.domain.services.text.base_text_service import TextService
from src.domain.services.text.extractor.base_regex import RegexPattern
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution

def detect_my_butthole(text: str) -> str:
    from langdetect import detect # type: ignore
    return detect(text) # type: ignore

# TODO: make a protocol spec for optimization
class ExtractSpeakersFromProtocol(TextService):
    def __init__(self, protocol: Protocol, country: Country, institution: Institution):
        self.protocol = protocol
        self.country = country
        self.institution = institution
        self.language_code = self._detect_language()

    def _detect_language(self) -> LanguageEnum:
        text = self.protocol.protocol_text.protocol_text
        lang_code = (detect_my_butthole(text)).upper()
        if hasattr(LanguageEnum, lang_code):
            return getattr(LanguageEnum, lang_code)
        raise ValueError(f"Detected language code '{lang_code}' is not supported by LanguageEnum.")

    def pick_pattern(self) -> type[RegexPattern] | None:
        pattern_cls = RegexPattern.find_by_specifications(
            country_code=self.country.country,
            institution_code=self.institution.type,
            language_code=self.language_code,
            protocol_type=self.protocol.protocol_type
        )
        return pattern_cls

    def process(self, protocol: Protocol, pattern_cls: type[RegexPattern]) -> List[Speech]:
        text = protocol.protocol_text.protocol_text
        pattern_instance = pattern_cls()
        protocol_id = self.protocol.id
        regex = pattern_instance.compile_pattern()
        matches = regex.findall(text)
        speeches: List[Speech] = []
        for match in matches:
            speech_uuid = UUID.new()
            text_uuid = UUID.new()
            speaker_name = match[0]
            speech_text = match[1]
            speaker = Speaker(id=UUID.new(), name=speaker_name, country_id=self.country.id)
            raw_text = RawText(id=UUID.new(), text=speech_text, speech_id=speech_uuid)
            text_obj = SpeechText(id=text_uuid, speech_id=speech_uuid, raw_text=raw_text.id, language_code=self.language_code)
            speech = Speech(
                id=speech_uuid,
                protocol_id=protocol_id,
                speaker_id=speaker.id,
                text=text_obj,
                metadata=None,
                metrics=None
            )
            speeches.append(speech)
        return speeches
