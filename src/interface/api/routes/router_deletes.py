from typing import Any
from fastapi import APIRouter, Depends
from src.application.di.di_text import (
    delete_protocol_use_case,
    delete_speech_use_case,
    delete_text_clean_use_case,
    delete_ngramized_text_use_case,
    delete_text_raw_use_case,
    delete_text_split_use_case,
    delete_tokenized_text_use_case,
    delete_translated_text_use_case,
    delete_speech_text_use_case,
)
from src.application.di.di_context import (
    delete_country_use_case,
    delete_institution_use_case,
    delete_party_use_case,
    delete_period_use_case,
    delete_speaker_use_case,
)
from src.domain.models.common.v_common import UUID

# FIXME: Needs tweaking of the schema for now does not properly delete protocols, maybe other things as well 
deletes_router = APIRouter()

@deletes_router.delete("/protocols/{protocol_id}")
def delete_protocol(protocol_id: str, use_case: Any = Depends(delete_protocol_use_case)):
    use_case.execute(UUID(protocol_id))
    return {"detail": "Protocol deleted"}

@deletes_router.delete("/speeches/{speech_id}")
def delete_speech(speech_id: str, use_case: Any = Depends(delete_speech_use_case)):
    use_case.execute(UUID(speech_id))
    return {"detail": "Speech deleted"}

@deletes_router.delete("/speech_texts/{speech_text_id}")
def delete_speech_text(speech_text_id: str, use_case: Any = Depends(delete_speech_text_use_case)):
    use_case.execute(UUID(speech_text_id))
    return {"detail": "SpeechText deleted"}

@deletes_router.delete("/text_clean/{clean_text_id}")
def delete_text_clean(clean_text_id: str, use_case: Any = Depends(delete_text_clean_use_case)):
    use_case.execute(UUID(clean_text_id))
    return {"detail": "CleanText deleted"}

@deletes_router.delete("/text_ngrams/{ngramized_text_id}")
def delete_ngramized_text(ngramized_text_id: str, use_case: Any = Depends(delete_ngramized_text_use_case)):
    use_case.execute(UUID(ngramized_text_id))
    return {"detail": "NGramizedText deleted"}

@deletes_router.delete("/text_raw/{raw_text_id}")
def delete_text_raw(raw_text_id: str, use_case: Any = Depends(delete_text_raw_use_case)):
    use_case.execute(UUID(raw_text_id))
    return {"detail": "RawText deleted"}

@deletes_router.delete("/text_split/{split_text_id}")
def delete_text_split(split_text_id: str, use_case: Any = Depends(delete_text_split_use_case)):
    use_case.execute(UUID(split_text_id))
    return {"detail": "TextSplit deleted"}

@deletes_router.delete("/text_tokenized/{tokenized_text_id}")
def delete_tokenized_text(tokenized_text_id: str, use_case: Any = Depends(delete_tokenized_text_use_case)):
    use_case.execute(UUID(tokenized_text_id))
    return {"detail": "TokenizedText deleted"}

@deletes_router.delete("/text_translated/{translated_text_id}")
def delete_translated_text(translated_text_id: str, use_case: Any = Depends(delete_translated_text_use_case)):
    use_case.execute(UUID(translated_text_id))
    return {"detail": "TranslatedText deleted"}

@deletes_router.delete("/countries/{country_id}")
def delete_country(country_id: str, use_case: Any = Depends(delete_country_use_case)):
    use_case.execute(country_id)
    return {"detail": "Country deleted"}

@deletes_router.delete("/institutions/{institution_id}")
def delete_institution(institution_id: str, use_case: Any = Depends(delete_institution_use_case)):
    use_case.execute(institution_id)
    return {"detail": "Institution deleted"}

@deletes_router.delete("/parties/{party_id}")
def delete_party(party_id: str, use_case: Any = Depends(delete_party_use_case)):
    use_case.execute(party_id)
    return {"detail": "Party deleted"}

@deletes_router.delete("/periods/{period_id}")
def delete_period(period_id: str, use_case: Any = Depends(delete_period_use_case)):
    use_case.execute(period_id)
    return {"detail": "Period deleted"}

@deletes_router.delete("/speakers/{speaker_id}")
def delete_speaker(speaker_id: str, use_case: Any = Depends(delete_speaker_use_case)):
    use_case.execute(speaker_id)
    return {"detail": "Speaker deleted"}
