class SpeechSentences:
    """A collection of sentences in a text."""
    
    def __init__(self, sentences: list[str] = []):
        self._sentences = sentences if sentences is not None else []

    @property
    def sentences(self) -> list[str]:
        return self._sentences

    @sentences.setter
    def sentences(self, value: list[str]):
        self._sentences = value if value is not None else []

    def __len__(self) -> int:
        """Get the number of sentences in the collection."""
        return len(self._sentences)