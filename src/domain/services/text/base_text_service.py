from abc import ABC, abstractmethod
from typing import Any
# from src.config import Config
# TODO: Pass config as class

class TextService(ABC):

    def __init__(self, config: Any):
        self.config = config

    @abstractmethod
    def process(self, *args: Any, **kwargs: Any) -> Any:
        """
        Process the input text and return the processed text.
        This method should be overridden by subclasses to implement specific text processing logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")
