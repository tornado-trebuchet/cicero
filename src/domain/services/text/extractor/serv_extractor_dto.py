from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class SpeakerDTO:
    name: str

@dataclass
class RawTextDTO:
    text: str

@dataclass
class SpeechDTO:
    speaker: SpeakerDTO
    raw_text: RawTextDTO
    language_code: str
    metadata: Optional[dict[str, Any]] = None
    metrics: Optional[dict[str, Any]] = None
