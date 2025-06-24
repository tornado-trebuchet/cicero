"""
N-gram tokenization module for generating n-gram tokens from preprocessed text.
Supports configurable n-gram sizes and language-aware processing.
"""
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import Counter
from itertools import combinations

from src.application.data_manipulation.base_manipulator import BaseManipulator, ProcessingContext
from src.application.data_manipulation.tokenize_preprocessed_text import TextTokenizer
from src.domain.models.v_enums import LanguageEnum
from src.domain.models.ve_text import Text
from src.config import DataManipulationConfig


class NGramTokenizer(BaseManipulator[Text, List[str]]):
    """
    N-gram tokenizer for generating n-gram tokens from text.
    
    Features:
    - Configurable n-gram sizes (1-gram to n-gram)
    - Frequency-based filtering
    - Language-aware n-gram generation
    - Integration with basic tokenization
    - Statistical analysis of n-grams
    """
    
    def __init__(self, config: Optional[DataManipulationConfig] = None):
        """Initialize n-gram tokenizer."""
        super().__init__(config)
        self._base_tokenizer = TextTokenizer(config)
        self._ngram_cache: Dict[str, List[str]] = {}
    
    def _generate_ngrams(self, tokens: List[str], n: int) -> List[str]:
        """
        Generate n-grams from a list of tokens.
        
        Args:
            tokens: List of tokens
            n: N-gram size
            
        Returns:
            List of n-gram strings
        """
        if not tokens or n <= 0 or n > len(tokens):
            return []
        
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i + n])
            ngrams.append(ngram)
        
        return ngrams
    
    def _generate_all_ngrams(self, tokens: List[str], min_n: int = 1, max_n: int = 3) -> List[str]:
        """
        Generate all n-grams within the specified range.
        
        Args:
            tokens: List of tokens
            min_n: Minimum n-gram size
            max_n: Maximum n-gram size
            
        Returns:
            List of all n-grams
        """
        all_ngrams = []
        
        for n in range(min_n, max_n + 1):
            ngrams = self._generate_ngrams(tokens, n)
            all_ngrams.extend(ngrams)
        
        return all_ngrams
    
    def _filter_ngrams_by_frequency(self, ngrams: List[str], min_freq: int) -> List[str]:
        """
        Filter n-grams by minimum frequency.
        
        Args:
            ngrams: List of n-grams
            min_freq: Minimum frequency threshold
            
        Returns:
            Filtered list of n-grams
        """
        if min_freq <= 1:
            return ngrams
        
        ngram_counts = Counter(ngrams)
        filtered_ngrams = [
            ngram for ngram, count in ngram_counts.items() 
            if count >= min_freq
        ]
        
        return filtered_ngrams
    
    def _apply_language_specific_ngram_rules(self, ngrams: List[str], language: LanguageEnum) -> List[str]:
        """
        Apply language-specific rules for n-gram processing.
        
        Args:
            ngrams: List of n-grams
            language: Language for processing
            
        Returns:
            Processed n-grams
        """
        if language == LanguageEnum.DE:
            # German-specific n-gram processing
            # Filter out n-grams with common function words at boundaries
            german_function_words = {'der', 'die', 'das', 'und', 'oder', 'aber', 'mit', 'von', 'zu', 'in', 'auf', 'für'}
            
            filtered_ngrams = []
            for ngram in ngrams:
                words = ngram.split()
                # Keep n-gram if it doesn't start or end with common function words (for longer n-grams)
                if len(words) > 2:
                    if words[0].lower() in german_function_words or words[-1].lower() in german_function_words:
                        continue
                filtered_ngrams.append(ngram)
            
            return filtered_ngrams
        
        elif language == LanguageEnum.FR:
            # French-specific n-gram processing
            # Filter out n-grams with common function words at boundaries
            french_function_words = {'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'avec', 'pour', 'sur', 'dans'}
            
            filtered_ngrams = []
            for ngram in ngrams:
                words = ngram.split()
                # Keep n-gram if it doesn't start or end with common function words (for longer n-grams)
                if len(words) > 2:
                    if words[0].lower() in french_function_words or words[-1].lower() in french_function_words:
                        continue
                filtered_ngrams.append(ngram)
            
            return filtered_ngrams
        
        return ngrams
    
    def _get_ngram_range(self) -> Tuple[int, int]:
        """Get n-gram range from configuration."""
        ngram_range = self.config.tokenization.ngram_range
        if isinstance(ngram_range, tuple) and len(ngram_range) == 2:
            return ngram_range
        else:
            # Default range
            return (1, 3)
    
    def process_single(self, data: Text, context: ProcessingContext) -> List[str]:
        """
        Process a single Text entity to generate n-gram tokens.
        
        Args:
            data: Text entity to process
            context: Processing context
            
        Returns:
            List of n-gram tokens
        """
        if not self._validate_input(data, context):
            return []
        
        # Use clean text if available, otherwise raw text
        text_to_process = data.clean_text or data.raw_text
        
        if not text_to_process or not text_to_process.strip():
            self.logger.warning("Empty text provided for n-gram tokenization")
            return []
        
        # Detect language
        language = data.language_code or self._detect_language(text_to_process, context)
        
        operation_name = f"ngram_tokenize_{language}"
        
        with self._operation_context(operation_name, context):
            # Get base tokens first
            if data.tokens:
                # Use existing tokens if available
                base_tokens = data.tokens
                self.logger.debug("Using existing tokens from text entity")
            else:
                # Generate tokens using base tokenizer
                base_tokens = self._base_tokenizer.process_single(data, context)
                self.logger.debug(f"Generated {len(base_tokens)} base tokens")
            
            if not base_tokens:
                self.logger.warning("No base tokens available for n-gram generation")
                return []
            
            # Get n-gram range from configuration
            min_n, max_n = self._get_ngram_range()
            
            # Generate all n-grams
            ngrams = self._generate_all_ngrams(base_tokens, min_n, max_n)
            
            if not ngrams:
                self.logger.warning("No n-grams generated")
                return []
            
            # Filter by frequency
            min_freq = self.config.tokenization.min_ngram_freq
            if min_freq > 1:
                ngrams = self._filter_ngrams_by_frequency(ngrams, min_freq)
                self.logger.debug(f"Filtered n-grams by frequency (min_freq={min_freq}): {len(ngrams)} remaining")
            
            # Apply language-specific rules
            ngrams = self._apply_language_specific_ngram_rules(ngrams, language)
            
            # Update text entity with n-gram tokens
            data.ngram_tokens = ngrams
            
            self.logger.debug(f"N-gram tokenization completed: {len(ngrams)} n-grams generated")
            
            return ngrams
    
    def generate_ngrams_from_tokens(self, tokens: List[str], language: Optional[LanguageEnum] = None, 
                                   min_n: int = 1, max_n: int = 3) -> List[str]:
        """
        Convenience method to generate n-grams from existing tokens.
        
        Args:
            tokens: List of tokens
            language: Optional language hint
            min_n: Minimum n-gram size
            max_n: Maximum n-gram size
            
        Returns:
            List of n-grams
        """
        if not tokens:
            return []
        
        # Generate all n-grams
        ngrams = self._generate_all_ngrams(tokens, min_n, max_n)
        
        # Apply language-specific rules if language is provided
        if language:
            ngrams = self._apply_language_specific_ngram_rules(ngrams, language)
        
        return ngrams
    
    def generate_ngrams_from_text(self, text: str, language: Optional[LanguageEnum] = None,
                                 min_n: int = 1, max_n: int = 3) -> List[str]:
        """
        Convenience method to generate n-grams from raw text.
        
        Args:
            text: Text to process
            language: Optional language hint
            min_n: Minimum n-gram size
            max_n: Maximum n-gram size
            
        Returns:
            List of n-grams
        """
        # First tokenize the text
        tokens = self._base_tokenizer.tokenize_clean_text(text, language)
        
        # Then generate n-grams
        return self.generate_ngrams_from_tokens(tokens, language, min_n, max_n)
    
    def get_ngram_statistics(self, ngrams: List[str]) -> Dict[str, Any]:
        """
        Generate statistics for n-grams.
        
        Args:
            ngrams: List of n-grams
            
        Returns:
            Dictionary with n-gram statistics
        """
        if not ngrams:
            return {
                'total_ngrams': 0,
                'unique_ngrams': 0,
                'ngram_distribution': {},
                'most_frequent_ngrams': {},
                'average_ngram_length': 0.0
            }
        
        # Count n-grams by size
        ngram_sizes = {}
        total_length = 0
        
        for ngram in ngrams:
            words = ngram.split()
            size = len(words)
            ngram_sizes[size] = ngram_sizes.get(size, 0) + 1
            total_length += len(ngram)
        
        # Frequency analysis
        ngram_freq = Counter(ngrams)
        
        return {
            'total_ngrams': len(ngrams),
            'unique_ngrams': len(ngram_freq),
            'ngram_distribution': ngram_sizes,
            'most_frequent_ngrams': dict(ngram_freq.most_common(10)),
            'average_ngram_length': total_length / len(ngrams) if ngrams else 0.0
        }
    
    def extract_significant_ngrams(self, text_entity: Text, context: ProcessingContext, 
                                  top_k: int = 20) -> List[Tuple[str, int]]:
        """
        Extract most significant n-grams from text.
        
        Args:
            text_entity: Text entity to analyze
            context: Processing context
            top_k: Number of top n-grams to return
            
        Returns:
            List of tuples (ngram, frequency)
        """
        ngrams = self.process_single(text_entity, context)
        
        if not ngrams:
            return []
        
        # Count frequencies
        ngram_freq = Counter(ngrams)
        
        # Return top k most frequent
        return ngram_freq.most_common(top_k)
    
    def compare_ngram_distributions(self, ngrams1: List[str], ngrams2: List[str]) -> Dict[str, Any]:
        """
        Compare n-gram distributions between two sets.
        
        Args:
            ngrams1: First set of n-grams
            ngrams2: Second set of n-grams
            
        Returns:
            Comparison statistics
        """
        freq1 = Counter(ngrams1)
        freq2 = Counter(ngrams2)
        
        # Find common and unique n-grams
        set1 = set(ngrams1)
        set2 = set(ngrams2)
        
        common = set1.intersection(set2)
        unique_to_1 = set1.difference(set2)
        unique_to_2 = set2.difference(set1)
        
        return {
            'total_ngrams_1': len(ngrams1),
            'total_ngrams_2': len(ngrams2),
            'unique_ngrams_1': len(set1),
            'unique_ngrams_2': len(set2),
            'common_ngrams': len(common),
            'unique_to_1': len(unique_to_1),
            'unique_to_2': len(unique_to_2),
            'jaccard_similarity': len(common) / len(set1.union(set2)) if set1.union(set2) else 0.0,
            'most_common_shared': [(ngram, freq1[ngram], freq2[ngram]) 
                                  for ngram, _ in Counter({k: min(freq1[k], freq2[k]) for k in common}).most_common(5)]
        }