"""
Text preprocessing module for cleaning and normalizing raw text.
Supports language-aware processing with configurable cleaning rules.
"""
import re
import unicodedata
from typing import Dict, Any, Optional

from src.application.data_manipulation.base_manipulator import BaseManipulator, ProcessingContext
from src.domain.models.v_enums import LanguageEnum
from src.domain.models.ve_text import Text
from src.config import DataManipulationConfig


class TextPreprocessor(BaseManipulator[Text, Text]):
    """
    Text preprocessing manipulator for cleaning and normalizing raw text.
    
    Features:
    - Language-aware text cleaning
    - Unicode normalization
    - Encoding handling
    - Whitespace normalization
    - Control character removal
    - Placeholder for future stopwords integration
    """
    
    def __init__(self, config: Optional[DataManipulationConfig] = None):
        """Initialize text preprocessor."""
        super().__init__(config)
        self._cleaning_patterns = self._initialize_cleaning_patterns()
    
    def _initialize_cleaning_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for text cleaning."""
        patterns = {
            # Control characters (except tab, newline, carriage return)
            'control_chars': re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]'),
            
            # Multiple whitespace
            'multiple_whitespace': re.compile(r'\s+'),
            
            # Leading/trailing whitespace
            'leading_trailing_ws': re.compile(r'^\s+|\s+$'),
            
            # Multiple line breaks
            'multiple_linebreaks': re.compile(r'\n\s*\n\s*\n+'),
            
            # Common XML/HTML entities (basic set)
            'xml_entities': re.compile(r'&(?:amp|lt|gt|quot|apos);'),
            
            # Zero-width characters
            'zero_width': re.compile(r'[\u200B-\u200D\uFEFF]'),
        }
        return patterns
    
    def _normalize_unicode(self, text: str) -> str:
        """Normalize Unicode characters."""
        if not self.config.text_processing.normalize_unicode:
            return text
        
        # NFC normalization - canonical decomposition followed by canonical composition
        normalized = unicodedata.normalize('NFC', text)
        
        self.logger.debug(f"Unicode normalization: {len(text)} -> {len(normalized)} chars")
        return normalized
    
    def _handle_encoding(self, text: str) -> str:
        """Handle encoding issues and cleanup."""
        try:
            # If text is already a string, just return it
            if isinstance(text, str):
                return text
                
            # If text is bytes, decode it
            if isinstance(text, bytes):
                for encoding in [self.config.text_processing.default_encoding] + self.config.text_processing.fallback_encodings:
                    try:
                        text = text.decode(encoding)
                        self.logger.debug(f"Successfully decoded with {encoding}")
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    # Fallback with error handling
                    text = text.decode(self.config.text_processing.default_encoding, errors='replace')
                    self.logger.warning("Used fallback decoding with replacement characters")
            
            return str(text)
            
        except Exception as e:
            self.logger.error(f"Encoding handling failed: {str(e)}")
            return str(text)  # Fallback to string conversion
    
    def _remove_control_characters(self, text: str) -> str:
        """Remove control characters while preserving important whitespace."""
        if not self.config.text_processing.remove_control_chars:
            return text
        
        # Remove control characters except tab, newline, carriage return
        cleaned = self._cleaning_patterns['control_chars'].sub('', text)
        
        # Remove zero-width characters
        cleaned = self._cleaning_patterns['zero_width'].sub('', cleaned)
        
        return cleaned
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace according to configuration."""
        if not self.config.text_processing.remove_extra_whitespace:
            return text
        
        # Handle line breaks
        if not self.config.text_processing.preserve_line_breaks:
            # Replace multiple line breaks with single ones
            text = self._cleaning_patterns['multiple_linebreaks'].sub('\n\n', text)
        
        # Replace multiple whitespace with single space
        text = self._cleaning_patterns['multiple_whitespace'].sub(' ', text)
        
        # Remove leading and trailing whitespace from each line
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        
        # Remove empty lines if not preserving line breaks
        if not self.config.text_processing.preserve_line_breaks:
            lines = [line for line in lines if line]
        
        return '\n'.join(lines) if self.config.text_processing.preserve_line_breaks else ' '.join(lines)
    
    def _clean_xml_entities(self, text: str) -> str:
        """Clean common XML/HTML entities."""
        entity_map = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&apos;': "'"
        }
        
        for entity, replacement in entity_map.items():
            text = text.replace(entity, replacement)
        
        return text
    
    def _apply_language_specific_cleaning(self, text: str, language: LanguageEnum) -> str:
        """Apply language-specific cleaning rules."""
        lang_config = self._get_language_config(language)
        
        # Language-specific cleaning can be added here
        # For now, we'll implement basic rules
        
        if language == LanguageEnum.DE:
            # German-specific cleaning
            # Remove common German parliamentary markers
            text = re.sub(r'\((?:Beifall|Heiterkeit|Zuruf|Widerspruch).*?\)', '', text)
            
        elif language == LanguageEnum.FR:
            # French-specific cleaning
            # Remove common French parliamentary markers
            text = re.sub(r'\((?:Applaudissements|Rires|Interruption).*?\)', '', text)
        
        return text
    
    def _prepare_for_stopwords_removal(self, text: str, language: LanguageEnum) -> str:
        """
        Prepare text for future stopwords removal.
        This is a placeholder for when stopwords repository is implemented.
        """
        # TODO: Integrate with stopwords repository when available
        # For now, just return the text as-is
        self.logger.debug(f"Stopwords removal placeholder for language: {language}")
        return text
    
    def process_single(self, data: Text, context: ProcessingContext) -> Text:
        """
        Process a single Text entity for cleaning and normalization.
        
        Args:
            data: Text entity to process
            context: Processing context
            
        Returns:
            Text entity with cleaned text
        """
        if not self._validate_input(data, context):
            return data
        
        raw_text = data.raw_text
        if not raw_text or not raw_text.strip():
            self.logger.warning("Empty or whitespace-only text provided")
            data.clean_text = ""
            return data
        
        # Detect language
        language = self._detect_language(raw_text, context)
        if data.language_code is None:
            data.language_code = language
        
        operation_name = f"preprocess_text_{language}"
        
        with self._operation_context(operation_name, context):
            # Step 1: Handle encoding
            cleaned_text = self._handle_encoding(raw_text)
            
            # Step 2: Normalize Unicode
            cleaned_text = self._normalize_unicode(cleaned_text)
            
            # Step 3: Remove control characters
            cleaned_text = self._remove_control_characters(cleaned_text)
            
            # Step 4: Clean XML entities
            cleaned_text = self._clean_xml_entities(cleaned_text)
            
            # Step 5: Apply language-specific cleaning
            cleaned_text = self._apply_language_specific_cleaning(cleaned_text, language)
            
            # Step 6: Normalize whitespace
            cleaned_text = self._normalize_whitespace(cleaned_text)
            
            # Step 7: Prepare for stopwords (placeholder)
            cleaned_text = self._prepare_for_stopwords_removal(cleaned_text, language)
            
            # Update the text entity
            data.clean_text = cleaned_text
            
            # Log cleaning statistics
            original_length = len(raw_text)
            cleaned_length = len(cleaned_text)
            reduction_percentage = ((original_length - cleaned_length) / original_length * 100) if original_length > 0 else 0
            
            self.logger.debug(
                f"Text cleaning completed: {original_length} -> {cleaned_length} chars "
                f"({reduction_percentage:.1f}% reduction)"
            )
            
            return data
    
    def preprocess_raw_text(self, raw_text: str, language: Optional[LanguageEnum] = None) -> str:
        """
        Convenience method to preprocess raw text directly.
        
        Args:
            raw_text: Raw text to preprocess
            language: Optional language hint
            
        Returns:
            Cleaned text string
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
        processed_text = self.process_single(temp_text, context)
        
        return processed_text.clean_text