from src.domain.models.text.a_protocol import Protocol
from src.interface.api.dtos.dto_text import ProtocolDTO
from src.domain.models.text.a_speech_text import SpeechText
from src.interface.api.dtos.dto_text import SpeechTextDTO
from src.domain.models.text.a_speech import Speech
from src.interface.api.dtos.dto_text import SpeechDTO

def protocol_to_dto(protocol: Protocol) -> ProtocolDTO:
    return ProtocolDTO(
        id=protocol.id.value,
        institution_id=protocol.institution_id.value,
        date=protocol.date.value,
        protocol_type=protocol.protocol_type,
        protocol_text=protocol.protocol_text.protocol_text,
        agenda=protocol.agenda.items if protocol.agenda else None,
        file_source=protocol.file_source.value if protocol.file_source else None,
        protocol_speeches=[s.value for s in protocol.protocol_speeches],
        metadata=protocol.metadata.get_properties() if protocol.metadata else None,
    )

def speech_text_to_dto(speech_text: SpeechText) -> SpeechTextDTO:
    return SpeechTextDTO(
        id=speech_text.id.value,
        speech_id=speech_text.speech_id.value,
        raw_text=speech_text.raw_text.value,
        language_code=speech_text.language_code,
        clean_text=speech_text.clean_text.value if speech_text.clean_text else None,
        translated_text=speech_text.translated_text.value if speech_text.translated_text else None,
        sentences=speech_text.sentences.value if speech_text.sentences else None,
        tokens=speech_text.tokens.value if speech_text.tokens else None,
        ngram_tokens=speech_text.ngram_tokens.value if speech_text.ngram_tokens else None,
        text_metrics={
            'word_count': speech_text.text_metrics.word_count if speech_text.text_metrics else None,
            'character_count': speech_text.text_metrics.character_count if speech_text.text_metrics else None,
            'token_count': speech_text.text_metrics.token_count if speech_text.text_metrics else None,
            'unique_token_count': speech_text.text_metrics.unique_token_count if speech_text.text_metrics else None,
            'sentence_count': speech_text.text_metrics.sentence_count if speech_text.text_metrics else None,
        } if speech_text.text_metrics else None
    )

def speech_to_dto(speech: Speech) -> SpeechDTO:
    return SpeechDTO(
        id=speech.id.value,
        protocol_id=speech.protocol_id.value,
        speaker_id=speech.speaker_id.value,
        text=speech.text.value,
        metrics={
            'dominant_topics': speech.metrics.dominant_topics if speech.metrics else None,
            'sentiment': speech.metrics.sentiment if speech.metrics else None,
            'dynamic_codes': speech.metrics.dynamic_codes if speech.metrics else None,
        } if speech.metrics else None,
        metadata=speech.metadata.get_properties() if speech.metadata else None,
    )
