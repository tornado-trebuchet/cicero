from src.domain.models.common.v_common import UUID
from domain.models.text.a_speech_text import SpeechText
from domain.models.text.e_text_raw import RawText
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_protocol import Protocol
from src.domain.services.text.base_text_service import TextService
from src.domain.services.utils.regex.base_regex import RegexPattern

class ExtractSpeakersFromProtocol(TextService):
    def __init__(self, protocol: Protocol):
        self.protocol = protocol

    def _pick_pattern(
        self,
        country_code=None,
        institution_code=None,
        language_code=None,
        protocol_type=None,
    ) -> type[RegexPattern] | None:
        """
        Find and return the regex pattern class matching the protocol's specifications.
        Returns the class, not an instance.
        """
        institution_code = self.protocol.institution_id
        protocol_type = self.protocol.protocol_type
        pattern_cls = RegexPattern.find_by_specifications(
            country_code=country_code,  
            institution_code=institution_code,
            language_code=language_code,
            protocol_type=protocol_type
        )
        return pattern_cls

    def _process(self, protocol: Protocol, pattern_cls: type[RegexPattern]) -> list[Speech]:
        text = protocol.protocol_text.protocol_text
        pattern_instance = pattern_cls()
        protocol_id = self.protocol.id
        language_code = pattern_instance.language_code or LanguageEnum.DE
        regex = pattern_instance.compile_pattern()
        matches = regex.findall(text)
        speeches = []
        for match in matches:
            speech_uuid = UUID.new()
            text_uuid = UUID.new()
            speaker_name = match[0]
            speech_text = match[1]
            speaker = Speaker(id=UUID.new(), name=speaker_name, country_id=self.protocol.country_id)
            text_obj = SpeechText(id=text_uuid, speech_id=speech_uuid, raw_text=RawText(speech_text), language_code=language_code)
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
