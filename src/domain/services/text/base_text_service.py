from abc import ABC, abstractmethod

class TextService(ABC):

    def __init__(self, config,):
        self.config = config
    
    @abstractmethod
    def process(self, *args, **kwargs):
        """
        Process the input text and return the processed text.
        This method should be overridden by subclasses to implement specific text processing logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def get_config(self):
        return self.config