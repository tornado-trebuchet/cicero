import re
import string
from src.domain.models.base_model import ValueObject

class CleanText(ValueObject):

    def __init__(self, text: str):
        self._text = text

    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value

    def num_words(self) -> int:
        return len(self._text.split())
    
    def num_characters(self, include_whitespace: bool = True, include_punctuation: bool = True) -> int:
        if not include_whitespace:
            text = ''.join(self._text.split())
        else:
            text = self._text
        
        if not include_punctuation:
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        return len(text)
    
    def num_sentences(self) -> int:       
        sentences = re.split(r'[.!?]+', self.text)
        return len([s for s in sentences if s.strip()])
    
    def split_sentences(self) -> list[str]:
        sentences = re.split(r'[.!?]+', self.text)
        return [s.strip() for s in sentences if s.strip()]

    def __str__(self) -> str:
        return self.text