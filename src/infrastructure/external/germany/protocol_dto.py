from dataclasses import dataclass
from typing import Optional, Any
from src.infrastructure.external.base_response import ResponseProtocol

@dataclass
class GermanResponseProtocolDTO(ResponseProtocol):
        date: str
        title: str
        source: str
        text: str
        institution: str
        type: str
        legislative_period: str
        label: str
        agenda:dict[str, list[str]]
        metadata:Optional[dict[str, Any]]