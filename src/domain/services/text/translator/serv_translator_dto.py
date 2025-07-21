from typing import List
from dataclasses import dataclass

@dataclass
class TranslatedTextDTO: 
    translation: List[str]