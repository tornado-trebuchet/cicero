import re
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

from src.application.data_manipulation.base_manipulator import BaseManipulator, ProcessingContext
from src.domain.models.v_enums import LanguageEnum
from src.domain.models.ve_text import Text
from src.config import DataManipulationConfig


@dataclass
class TextMetrics:
    word_count: int
    character_count: int
    character_count_no_spaces: int
    token_count: int
    unique_token_count: int
    sentence_count: int
    paragraph_count: int
    average_word_length: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'word_count': self.word_count,
            'character_count': self.character_count,
            'character_count_no_spaces': self.character_count_no_spaces,
            'token_count': self.token_count,
            'unique_token_count': self.unique_token_count,
            'sentence_count': self.sentence_count,
            'paragraph_count': self.paragraph_count,
            'average_word_length': self.average_word_length
        }


class TextLengthCounter(BaseManipulator[Text, TextMetrics]):
    """
    Text length counter for calculating various text metrics.
    
    Features:
    - Multiple word counting methods
    - Character counting with/without spaces
    - Token counting with uniqueness
    - Sentence and paragraph counting
    - Language-aware counting rules
    - Average word length calculation
    """
    
    def __init__(self, config: DataManipulationConfig):
        super().__init__(config)
        self._counting_patterns = self._initialize_counting_patterns()
    
    def _initialize_counting_patterns(self) -> Dict[str, re.Pattern]:
        patterns = {
            # Word boundaries (whitespace-based)
            'whitespace_words': re.compile(r'\S+'),
            
            # Sentence boundaries (basic)
            'sentences': re.compile(r'[.!?]+\s+'),
            
            # Paragraph boundaries
            'paragraphs': re.compile(r'\n\s*\n'),
            
            # Linguistic word boundaries (more sophisticated)
            'linguistic_words': re.compile(r'\b\w+\b'),
            
            # Token boundaries (alphanumeric sequences)
            'tokens': re.compile(r'\w+'),
            
            # Punctuation
            'punctuation': re.compile(r'[^\w\s]'),
        }
        return patterns
    
    def _count_words_whitespace(self, text: str) -> int:
        if not text.strip():
            return 0
        return len(self._counting_patterns['whitespace_words'].findall(text))
    
    def _count_words_linguistic(self, text: str, language: LanguageEnum) -> int:
        if not text.strip():
            return 0
        
        # Basic linguistic word counting
        words = self._counting_patterns['linguistic_words'].findall(text)
        
        # Apply language-specific rules
        lang_config = self._get_language_config(language)
        
        if language == LanguageEnum.DE:
            words = [word for word in words if len(word) > 1 or word.lower() in ['a', 'i']]
        
        elif language == LanguageEnum.FR:
            words = [word for word in words if len(word) > 1 or word.lower() in ['a', 'à', 'y']]
        
        return len(words)
    
    def _count_words_tokenized(self, tokens: list[str]) -> int:
        if not tokens:
            return 0
        
        valid_tokens = [
            token for token in tokens 
            if (token.strip() and 
                len(token) >= self.config.tokenization.min_token_length and
                len(token) <= self.config.tokenization.max_token_length)
        ]
        
        return len(valid_tokens)
    
    def _count_characters(self, text: str, include_whitespace: bool = True, include_punctuation: bool = True) -> int:
        if not text:
            return 0
        
        if not include_whitespace:
            text = re.sub(r'\s', '', text)
        
        if not include_punctuation:
            text = self._counting_patterns['punctuation'].sub('', text)
        
        return len(text)
    
    def _count_tokens(self, text: str) -> Tuple[int, int]:
        if not text.strip():
            return 0, 0
        
        tokens = self._counting_patterns['tokens'].findall(text.lower())
        
        valid_tokens = [
            token for token in tokens 
            if (len(token) >= self.config.tokenization.min_token_length and
                len(token) <= self.config.tokenization.max_token_length)
        ]
        
        total_tokens = len(valid_tokens)
        unique_tokens = len(set(valid_tokens)) if valid_tokens else 0
        
        return total_tokens, unique_tokens
    
    def _count_sentences(self, text: str, language: LanguageEnum) -> int:
        if not text.strip():
            return 0
        
        # Basic sentence counting
        sentences = self._counting_patterns['sentences'].split(text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Adjust for text that doesn't end with sentence terminator
        if text.strip() and not re.search(r'[.!?]\s*$', text.strip()):
            sentence_count += 1
        
        return max(1, sentence_count)
    
    def _count_paragraphs(self, text: str) -> int:
        if not text.strip():
            return 0
        
        paragraphs = self._counting_patterns['paragraphs'].split(text)
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        return max(1, paragraph_count)
    
    def _calculate_average_word_length(self, text: str, word_count: int) -> float:
        if word_count == 0:
            return 0.0
        
        words = self._counting_patterns['linguistic_words'].findall(text)
        if not words:
            return 0.0
        
        total_length = sum(len(word) for word in words)
        return total_length / len(words)
    
    def process_single(self, data: Text, context: ProcessingContext) -> TextMetrics:

        if not self._validate_input(data, context):
            return TextMetrics(0, 0, 0, 0, 0, 0, 0, 0.0)
        
        # Use clean text if available, otherwise raw text
        text_to_analyze = data.clean_text or data.raw_text
        language = data.language_code

        if not text_to_analyze or not text_to_analyze.strip():
            self.logger.warning("Empty text provided for counting")
            return TextMetrics(0, 0, 0, 0, 0, 0, 0, 0.0)
        
        operation_name = f"count_text_metrics_{language}"
        
        with self._operation_context(operation_name, context):
            # Word counting based on configured method
            count_method = self.config.counting.count_method
            
            if count_method == "whitespace":
                word_count = self._count_words_whitespace(text_to_analyze)
            elif count_method == "tokenized" and data.tokens:
                word_count = self._count_words_tokenized(data.tokens)
            elif count_method == "linguistic":
                word_count = self._count_words_linguistic(text_to_analyze, language)
            else:
                word_count = self._count_words_whitespace(text_to_analyze)
            
            # Character counting
            char_count = self._count_characters(
                text_to_analyze,
                include_whitespace=True,
                include_punctuation=self.config.counting.include_punctuation
            )
            
            char_count_no_spaces = self._count_characters(
                text_to_analyze,
                include_whitespace=self.config.counting.include_whitespace,
                include_punctuation=self.config.counting.include_punctuation
            )
            
            # Token counting
            token_count, unique_token_count = self._count_tokens(text_to_analyze)
            
            # Sentence and paragraph counting
            sentence_count = self._count_sentences(text_to_analyze, language)
            paragraph_count = self._count_paragraphs(text_to_analyze)
            
            # Average word length
            avg_word_length = self._calculate_average_word_length(text_to_analyze, word_count)
            
            metrics = TextMetrics(
                word_count=word_count,
                character_count=char_count,
                character_count_no_spaces=char_count_no_spaces,
                token_count=token_count,
                unique_token_count=unique_token_count,
                sentence_count=sentence_count,
                paragraph_count=paragraph_count,
                average_word_length=avg_word_length
            )
            
            # Update text entity with word count
            data.word_count = word_count
            
            self.logger.debug(f"Text metrics calculated: {metrics.to_dict()}")
            
            return metrics
    
    def update_text_entity_metrics(self, text_entity: Text, context: Optional[ProcessingContext] = None) -> Text:
        """
        Update a Text entity with calculated metrics.
        
        Args:
            text_entity: Text entity to update
            context: Optional processing context
            
        Returns:
            Updated text entity
        """
        if context is None:
            context = ProcessingContext()
        
        metrics = self.process_single(text_entity, context)
        text_entity.word_count = metrics.word_count
        
        return text_entity