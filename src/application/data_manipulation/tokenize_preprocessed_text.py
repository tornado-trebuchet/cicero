"""
Tokenization module for converting cleaned text into tokens.
Supports language-aware tokenization with configurable rules.
"""
import re
from typing import List, Dict, Any, Optional, Set

from src.application.data_manipulation.base_manipulator import BaseManipulator, ProcessingContext
from src.domain.models.v_enums import LanguageEnum
from src.domain.models.ve_text import Text
from src.config import DataManipulationConfig


class TextTokenizer(BaseManipulator[Text, List[str]]):
    """
    Text tokenizer for converting cleaned text into tokens.
    
    Features:
    - Language-aware tokenization rules
    - Configurable token filtering
    - Integration with text preprocessing
    - Token normalization
    - Support for different tokenization strategies
    """
    
    def __init__(self, config: Optional[DataManipulationConfig] = None):
        """Initialize text tokenizer."""
        super().__init__(config)
        self._tokenization_patterns = self._initialize_tokenization_patterns()
        self._language_specific_rules = self._initialize_language_rules()
    
    def _initialize_tokenization_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for tokenization."""
        patterns = {
            # Basic word tokenization
            'words': re.compile(r'\b\w+\b'),
            
            # Alphanumeric tokens
            'alphanumeric': re.compile(r'\w+'),
            
            # Words with apostrophes (for contractions)
            'words_with_apostrophes': re.compile(r"\b\w+(?:'\w+)?\b"),
            
            # Punctuation
            'punctuation': re.compile(r'[^\w\s]'),
            
            # Numbers
            'numbers': re.compile(r'\b\d+(?:\.\d+)?\b'),
            
            # Whitespace
            'whitespace': re.compile(r'\s+'),
            
            # German compound separators
            'german_compounds': re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])'),
            
            # French elisions and contractions
            'french_contractions': re.compile(r"\b(?:l'|d'|c'|s'|n'|m'|t'|j')"),
        }
        return patterns
    
    def _initialize_language_rules(self) -> Dict[LanguageEnum, Dict[str, Any]]:
        """Initialize language-specific tokenization rules."""
        return {
            LanguageEnum.DE: {
                'preserve_compounds': True,
                'split_contractions': False,
                'case_sensitive': False,
                'min_token_length': 2,
                'special_chars': ['ä', 'ö', 'ü', 'ß'],
                'prefixes': ['un', 'vor', 'nach', 'über', 'unter'],
                'suffixes': ['ung', 'heit', 'keit', 'lich', 'isch']
            },
            LanguageEnum.FR: {
                'preserve_compounds': False,
                'split_contractions': True,
                'case_sensitive': False,
                'min_token_length': 2,
                'special_chars': ['à', 'é', 'è', 'ê', 'ë', 'î', 'ô', 'ù', 'û', 'ü', 'ÿ', 'ç'],
                'contractions': ["l'", "d'", "c'", "s'", "n'", "m'", "t'", "j'"],
                'elisions': ['que', 'jusque', 'lorsque', 'puisque']
            }
        }
    
    def _basic_tokenize(self, text: str) -> List[str]:
        """Perform basic tokenization."""
        if not text.strip():
            return []
        
        # Use words with apostrophes pattern to handle contractions
        tokens = self._tokenization_patterns['words_with_apostrophes'].findall(text.lower())
        
        # Filter by length constraints
        min_length = self.config.tokenization.min_token_length
        max_length = self.config.tokenization.max_token_length
        
        filtered_tokens = [
            token for token in tokens 
            if min_length <= len(token) <= max_length
        ]
        
        return filtered_tokens
    
    def _apply_german_tokenization(self, text: str) -> List[str]:
        """Apply German-specific tokenization rules."""
        rules = self._language_specific_rules[LanguageEnum.DE]
        
        # Basic tokenization
        tokens = self._basic_tokenize(text)
        
        if rules['preserve_compounds']:
            # Keep compound words intact - don't split them
            # This is the default behavior with basic tokenization
            pass
        
        # Handle German special characters
        # Already handled in basic tokenization with Unicode support
        
        # Apply minimum token length (German-specific)
        min_length = rules['min_token_length']
        tokens = [token for token in tokens if len(token) >= min_length]
        
        return tokens
    
    def _apply_french_tokenization(self, text: str) -> List[str]:
        """Apply French-specific tokenization rules."""
        rules = self._language_specific_rules[LanguageEnum.FR]
        
        if rules['split_contractions']:
            # Handle French contractions and elisions
            text = self._handle_french_contractions(text)
        
        # Basic tokenization
        tokens = self._basic_tokenize(text)
        
        # Apply minimum token length (French-specific)
        min_length = rules['min_token_length']
        tokens = [token for token in tokens if len(token) >= min_length]
        
        return tokens
    
    def _handle_french_contractions(self, text: str) -> str:
        """Handle French contractions and elisions."""
        rules = self._language_specific_rules[LanguageEnum.FR]
        
        # Split common contractions
        contractions_map = {
            "l'": "le ",
            "d'": "de ",
            "c'": "ce ",
            "s'": "se ",
            "n'": "ne ",
            "m'": "me ",
            "t'": "te ",
            "j'": "je "
        }
        
        for contraction, expansion in contractions_map.items():
            text = text.replace(contraction, expansion)
        
        return text
    
    def _normalize_tokens(self, tokens: List[str], language: LanguageEnum) -> List[str]:
        """Normalize tokens according to configuration and language rules."""
        if not tokens:
            return []
        
        normalized = []
        
        for token in tokens:
            # Convert to lowercase if configured
            if self.config.tokenization.lowercase_tokens:
                token = token.lower()
            
            # Remove punctuation if configured
            if self.config.tokenization.remove_punctuation:
                token = self._tokenization_patterns['punctuation'].sub('', token)
            
            # Skip empty tokens after processing
            if not token.strip():
                continue
            
            # Apply final length check
            if (len(token) >= self.config.tokenization.min_token_length and
                len(token) <= self.config.tokenization.max_token_length):
                normalized.append(token)
        
        return normalized
    
    def _filter_stopwords_placeholder(self, tokens: List[str], language: LanguageEnum) -> List[str]:
        """
        Placeholder for stopwords filtering.
        Will be implemented when stopwords repository is available.
        """
        # TODO: Integrate with stopwords repository when available
        self.logger.debug(f"Stopwords filtering placeholder for {len(tokens)} tokens in {language}")
        return tokens
    
    def process_single(self, data: Text, context: ProcessingContext) -> List[str]:
        """
        Process a single Text entity to generate tokens.
        
        Args:
            data: Text entity to tokenize
            context: Processing context
            
        Returns:
            List of tokens
        """
        if not self._validate_input(data, context):
            return []
        
        # Use clean text if available, otherwise raw text
        text_to_tokenize = data.clean_text or data.raw_text
        
        if not text_to_tokenize or not text_to_tokenize.strip():
            self.logger.warning("Empty text provided for tokenization")
            return []
        
        # Detect language
        language = data.language_code or self._detect_language(text_to_tokenize, context)
        
        operation_name = f"tokenize_text_{language}"
        
        with self._operation_context(operation_name, context):
            # Apply language-specific tokenization
            if language == LanguageEnum.DE:
                tokens = self._apply_german_tokenization(text_to_tokenize)
            elif language == LanguageEnum.FR:
                tokens = self._apply_french_tokenization(text_to_tokenize)
            else:
                # Fallback to basic tokenization
                tokens = self._basic_tokenize(text_to_tokenize)
                self.logger.debug(f"Using basic tokenization for language: {language}")
            
            # Normalize tokens
            tokens = self._normalize_tokens(tokens, language)
            
            # Apply stopwords filtering (placeholder)
            tokens = self._filter_stopwords_placeholder(tokens, language)
            
            # Update text entity with tokens
            data.tokens = tokens
            
            self.logger.debug(f"Tokenization completed: {len(tokens)} tokens generated")
            
            return tokens
    
    def tokenize_raw_text(self, raw_text: str, language: Optional[LanguageEnum] = None) -> List[str]:
        """
        Convenience method to tokenize raw text directly.
        
        Args:
            raw_text: Raw text to tokenize
            language: Optional language hint
            
        Returns:
            List of tokens
        """
        from src.domain.models.v_common import UUID
        
        # Create temporary Text entity
        temp_text = Text(
            id=UUID.new(),
            speech_id=UUID.new(),
            raw_text=raw_text,
            language_code=language
        )
        
        context = ProcessingContext(language=language)
        return self.process_single(temp_text, context)
    
    def tokenize_clean_text(self, clean_text: str, language: Optional[LanguageEnum] = None) -> List[str]:
        """
        Convenience method to tokenize clean text directly.
        
        Args:
            clean_text: Clean text to tokenize
            language: Optional language hint
            
        Returns:
            List of tokens
        """
        from src.domain.models.v_common import UUID
        
        # Create temporary Text entity with clean text
        temp_text = Text(
            id=UUID.new(),
            speech_id=UUID.new(),
            raw_text="",  # Empty raw text since we're using clean text
            clean_text=clean_text,
            language_code=language
        )
        
        context = ProcessingContext(language=language)
        return self.process_single(temp_text, context)
    
    def get_token_statistics(self, tokens: List[str]) -> Dict[str, Any]:
        """
        Generate statistics for a list of tokens.
        
        Args:
            tokens: List of tokens to analyze
            
        Returns:
            Dictionary with token statistics
        """
        if not tokens:
            return {
                'total_tokens': 0,
                'unique_tokens': 0,
                'average_token_length': 0.0,
                'min_token_length': 0,
                'max_token_length': 0,
                'token_frequency': {}
            }
        
        from collections import Counter
        
        token_freq = Counter(tokens)
        token_lengths = [len(token) for token in tokens]
        
        return {
            'total_tokens': len(tokens),
            'unique_tokens': len(token_freq),
            'average_token_length': sum(token_lengths) / len(token_lengths),
            'min_token_length': min(token_lengths),
            'max_token_length': max(token_lengths),
            'token_frequency': dict(token_freq.most_common(10))  # Top 10 most frequent
        }