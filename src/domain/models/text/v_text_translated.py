from src.domain.models.base_model import ValueObject

class TranslatedText(ValueObject):
    """Value object for translated text to english"""
    
    def __init__(self, translated_text: str):
        self._translated_text = translated_text

    @property
    def value(self) -> str:
        return self.value
