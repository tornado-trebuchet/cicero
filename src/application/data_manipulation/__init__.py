"""
Data manipulation module for Cicero application.

This package provides comprehensive text processing and analysis capabilities
for parliamentary speech data, including:

- Text preprocessing and cleaning
- Tokenization and n-gram generation  
- Text length and metrics calculation
- Speaker extraction from parliamentary protocols
- Configurable language-aware processing

All modules support German and French language processing with configurable
parameters through the DataManipulationConfig system.
"""

from .base_manipulator import BaseManipulator, ProcessingContext, ProgressInfo
from .preprocess_text import TextPreprocessor
from .count_text_length import TextLengthCounter
from .tokenize_preprocessed_text import TextTokenizer
from .tokenize_with_ngrams import NGramTokenizer
from .extract_speakers_with_regex import SpeakerExtractor

__all__ = [
    'BaseManipulator',
    'ProcessingContext', 
    'ProgressInfo',
    'TextPreprocessor',
    'TextLengthCounter',
    'TextTokenizer',
    'NGramTokenizer',
    'SpeakerExtractor'
]
