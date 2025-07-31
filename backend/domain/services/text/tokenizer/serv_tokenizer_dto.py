from typing import List
from dataclasses import dataclass


@dataclass
class TokenizedTextDTO:
    tokens: List[str]
