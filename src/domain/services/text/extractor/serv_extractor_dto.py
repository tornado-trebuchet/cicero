from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class SpeakerDTO:
    name: str
    land: Optional[str] = None
    party: Optional[str] = None


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
