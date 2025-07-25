from typing import List

from src.application.modules.text_services.extractor.extractor_spec import (
    ExtractionSpec,
)
from src.domain.models.text.a_protocol import Protocol
from src.domain.services.text.base_text_service import TextService
from src.domain.services.text.extractor.regex.base_regex import RegexPattern
from src.domain.services.text.extractor.serv_extractor_dto import (
    RawTextDTO,
    SpeakerDTO,
    SpeechDTO,
)

# TODO: Since we do not need a universal regex anymore.
# And can easily swap them, then we should probably decouple this from regex implementation


# also: (self, Protocol, Country, Institution, Language, PatternSpec)
class ExtractSpeakersFromProtocol(TextService):
    def __init__(self, protocol: Protocol, spec: ExtractionSpec):  # FIXME: SHOULD NOT DEPEND ON EXTERNALS
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
            protocol_type=self.protocol.protocol_type,
        )
        return pattern_cls

    def process(self, protocol: Protocol, pattern_cls: type[RegexPattern]) -> List[SpeechDTO]:
        text = protocol.protocol_text.protocol_text
        pattern_instance = pattern_cls()
        regex = pattern_instance.compile_pattern()
        matches = list(regex.finditer(text))
        speeches: List[SpeechDTO] = []
        for idx, match in enumerate(matches):
            speaker_name = match.group(1)
            speaker_land = match.group(2) if match.group(2) else None
            speaker_party = match.group(3) if match.group(3) else None
            # speaker_role = match.group(4) # IN QUESTION
            start = match.end()
            if idx + 1 < len(matches):
                end = matches[idx + 1].start()
            else:
                end = len(text)
            speech_text = text[start:end].strip()
            # Add the first letter of the speech I AM SORRY FOR THAT!
            first_letter = match.group(match.lastindex) if match.lastindex else ""
            if speech_text:
                speech_text = (
                    first_letter + speech_text[0:]
                )
            else:
                speech_text = first_letter
            speaker_dto = SpeakerDTO(name=speaker_name,land=speaker_land, party=speaker_party)
            raw_text_dto = RawTextDTO(text=speech_text)
            speech_dto = SpeechDTO(
                speaker=speaker_dto,
                raw_text=raw_text_dto,
                language_code=self.language,
                metadata=None,
                metrics=None,
            )
            speeches.append(speech_dto)
        return speeches
