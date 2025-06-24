"""
Speaker extraction module using regex patterns to find speakers in raw text.
Divides protocol into domain desired structure and extracts speaker metadata.
"""
import re
from typing import List, Dict, Any, Optional, Tuple, NamedTuple
from dataclasses import dataclass
from enum import Enum

from src.application.data_manipulation.base_manipulator import BaseManipulator, ProcessingContext
from src.domain.models.v_enums import LanguageEnum, CountryEnum, GenderEnum
from src.domain.models.v_common import UUID
from src.domain.models.ve_speaker import Speaker
from src.domain.models.e_regex_pattern import RegexPattern
from src.domain.irepository.i_regex_pattern import IRegexPatternRepository
from src.config import DataManipulationConfig


class ExtractionMethod(Enum):
    """Methods for pattern selection and extraction."""
    ACTIVE_PATTERNS_ONLY = "active_only"
    ALL_PATTERNS = "all_patterns"
    PRIORITY_ORDER = "priority_order"
    BEST_MATCH = "best_match"


@dataclass
class SpeakerMatch:
    """Container for speaker extraction match results."""
    speaker_name: str
    raw_match: str
    start_position: int
    end_position: int
    pattern_id: Optional[UUID] = None
    pattern_description: Optional[str] = None
    confidence_score: float = 1.0
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SpeechSegment:
    """Container for extracted speech segments."""
    speaker_match: SpeakerMatch
    text_content: str
    start_position: int
    end_position: int
    segment_order: int
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SpeakerExtractor(BaseManipulator[str, List[SpeechSegment]]):
    """
    Speaker extractor for identifying speakers and segmenting text.
    
    Features:
    - Regex pattern-based speaker extraction
    - Integration with RegexPattern repository
    - Context-aware pattern selection
    - Speaker metadata extraction
    - Text segmentation by speakers
    - Support for multiple extraction strategies
    """
    
    def __init__(self, config: Optional[DataManipulationConfig] = None, 
                 regex_repository: Optional[IRegexPatternRepository] = None):
        """Initialize speaker extractor."""
        super().__init__(config)
        self._regex_repository = regex_repository
        self._pattern_cache: Dict[str, List[RegexPattern]] = {}
        self._compiled_patterns: Dict[UUID, re.Pattern] = {}
    
    def set_regex_repository(self, repository: IRegexPatternRepository) -> None:
        """Set the regex pattern repository."""
        self._regex_repository = repository
        self._clear_cache()
    
    def _clear_cache(self) -> None:
        """Clear pattern caches."""
        self._pattern_cache.clear()
        self._compiled_patterns.clear()
    
    def _get_patterns_for_context(self, context: ProcessingContext) -> List[RegexPattern]:
        """
        Get regex patterns for the given context.
        
        Args:
            context: Processing context with country, institution, period info
            
        Returns:
            List of applicable regex patterns
        """
        if not self._regex_repository:
            self.logger.warning("No regex repository available")
            return []
        
        # Validate required context
        if not context.country or not context.institution_id:
            self.logger.warning("Missing required context: country and institution_id")
            return []
        
        # Create cache key
        cache_key = f"{context.country}_{context.institution_id}_{context.period_id}"
        
        # Check cache first
        if cache_key in self._pattern_cache:
            return self._pattern_cache[cache_key]
        
        try:
            # Convert country enum to UUID - this would need proper mapping in real implementation
            # For now, we'll return empty list and log the issue
            self.logger.error("Need to implement country enum to UUID mapping for regex repository")
            return []
            
        except Exception as e:
            self.logger.error(f"Error retrieving patterns: {str(e)}")
            return []
    
    def _compile_pattern(self, regex_pattern: RegexPattern) -> Optional[re.Pattern]:
        """
        Compile regex pattern with caching.
        
        Args:
            regex_pattern: RegexPattern entity
            
        Returns:
            Compiled regex pattern or None if compilation fails
        """
        if regex_pattern.id in self._compiled_patterns:
            return self._compiled_patterns[regex_pattern.id]
        
        try:
            # Compile with multiline and case-insensitive flags
            compiled = re.compile(regex_pattern.pattern, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            self._compiled_patterns[regex_pattern.id] = compiled
            return compiled
            
        except re.error as e:
            self.logger.error(f"Failed to compile pattern {regex_pattern.id}: {str(e)}")
            return None
    
    def _extract_speaker_matches(self, text: str, patterns: List[RegexPattern]) -> List[SpeakerMatch]:
        """
        Extract speaker matches from text using provided patterns.
        
        Args:
            text: Text to search
            patterns: List of regex patterns to apply
            
        Returns:
            List of speaker matches
        """
        all_matches = []
        
        for pattern in patterns:
            compiled_pattern = self._compile_pattern(pattern)
            if not compiled_pattern:
                continue
            
            try:
                # Find all matches
                for match in compiled_pattern.finditer(text):
                    # Extract speaker name (assume first capture group or whole match)
                    speaker_name = match.group(1) if match.groups() else match.group(0)
                    
                    # Clean and normalize speaker name
                    speaker_name = self._normalize_speaker_name(speaker_name)
                    
                    if speaker_name:  # Only add if we have a valid speaker name
                        speaker_match = SpeakerMatch(
                            speaker_name=speaker_name,
                            raw_match=match.group(0),
                            start_position=match.start(),
                            end_position=match.end(),
                            pattern_id=pattern.id,
                            pattern_description=pattern.description,
                            confidence_score=self._calculate_confidence_score(match, pattern),
                            metadata={
                                'pattern_version': pattern.version,
                                'match_groups': match.groups()
                            }
                        )
                        all_matches.append(speaker_match)
                        
            except Exception as e:
                self.logger.error(f"Error applying pattern {pattern.id}: {str(e)}")
                continue
        
        # Sort matches by position
        all_matches.sort(key=lambda m: m.start_position)
        
        return all_matches
    
    def _normalize_speaker_name(self, raw_name: str) -> str:
        """
        Normalize extracted speaker name.
        
        Args:
            raw_name: Raw extracted speaker name
            
        Returns:
            Normalized speaker name
        """
        if not raw_name:
            return ""
        
        # Remove common prefixes and suffixes
        name = raw_name.strip()
        
        # Remove common parliamentary titles and markers
        title_patterns = [
            r'^(?:Herr|Frau|Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Prof\.?)\s+',
            r'\s*\(.*?\)\s*$',  # Remove parenthetical content
            r'^\s*[-–—]\s*',     # Remove leading dashes
            r'\s*[-–—]\s*$',     # Remove trailing dashes
            r'^\s*[:\-]\s*',     # Remove leading colons/dashes
        ]
        
        for pattern in title_patterns:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Clean up whitespace
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Capitalize properly
        if self.config.speaker_extraction.normalize_speaker_names:
            name = self._proper_case_name(name)
        
        return name
    
    def _proper_case_name(self, name: str) -> str:
        """Apply proper case formatting to names."""
        if not name:
            return name
        
        # Split on spaces and hyphens
        parts = re.split(r'([\s\-])', name)
        
        formatted_parts = []
        for part in parts:
            if part.isalpha() and len(part) > 1:
                # Capitalize first letter, lowercase the rest
                formatted_parts.append(part[0].upper() + part[1:].lower())
            else:
                formatted_parts.append(part)
        
        return ''.join(formatted_parts)
    
    def _calculate_confidence_score(self, match: re.Match, pattern: RegexPattern) -> float:
        """
        Calculate confidence score for a match.
        
        Args:
            match: Regex match object
            pattern: RegexPattern that produced the match
            
        Returns:
            Confidence score between 0 and 1
        """
        base_score = 1.0
        
        # Reduce score for very short matches
        match_text = match.group(0)
        if len(match_text) < 3:
            base_score *= 0.5
        
        # Increase score for patterns with higher version numbers (more refined)
        if pattern.version and pattern.version > 1:
            base_score *= min(1.2, 1.0 + (pattern.version - 1) * 0.1)
        
        # Ensure score stays within bounds
        return min(1.0, max(0.0, base_score))
    
    def _segment_text_by_speakers(self, text: str, speaker_matches: List[SpeakerMatch]) -> List[SpeechSegment]:
        """
        Segment text based on speaker matches.
        
        Args:
            text: Full text to segment
            speaker_matches: List of speaker matches
            
        Returns:
            List of speech segments
        """
        if not speaker_matches:
            return []
        
        segments = []
        
        for i, match in enumerate(speaker_matches):
            # Determine the end position for this segment
            if i + 1 < len(speaker_matches):
                # Next speaker starts the end of this segment
                segment_end = speaker_matches[i + 1].start_position
            else:
                # Last segment goes to end of text
                segment_end = len(text)
            
            # Extract text content (after the speaker marker)
            content_start = match.end_position
            text_content = text[content_start:segment_end].strip()
            
            if text_content:  # Only create segment if there's actual content
                segment = SpeechSegment(
                    speaker_match=match,
                    text_content=text_content,
                    start_position=content_start,
                    end_position=segment_end,
                    segment_order=i + 1,
                    metadata={
                        'total_segments': len(speaker_matches),
                        'content_length': len(text_content)
                    }
                )
                segments.append(segment)
        
        return segments
    
    def _resolve_duplicate_speakers(self, speaker_matches: List[SpeakerMatch]) -> List[SpeakerMatch]:
        """
        Resolve duplicate or conflicting speaker matches.
        
        Args:
            speaker_matches: List of speaker matches
            
        Returns:
            Deduplicated speaker matches
        """
        if not speaker_matches:
            return []
        
        # Group matches by position overlap
        resolved_matches = []
        i = 0
        
        while i < len(speaker_matches):
            current_match = speaker_matches[i]
            conflicting_matches = [current_match]
            
            # Find all matches that overlap with current
            j = i + 1
            while j < len(speaker_matches):
                next_match = speaker_matches[j]
                if (next_match.start_position < current_match.end_position and
                    next_match.end_position > current_match.start_position):
                    conflicting_matches.append(next_match)
                    j += 1
                else:
                    break
            
            # Choose the best match from conflicting ones
            if len(conflicting_matches) > 1:
                # Sort by confidence score, then by pattern specificity
                best_match = max(conflicting_matches, 
                               key=lambda m: (m.confidence_score, len(m.speaker_name)))
                resolved_matches.append(best_match)
                i = j  # Skip all conflicting matches
            else:
                resolved_matches.append(current_match)
                i += 1
        
        return resolved_matches
    
    def process_single(self, data: str, context: ProcessingContext) -> List[SpeechSegment]:
        """
        Process raw text to extract speakers and segment speech.
        
        Args:
            data: Raw text (XML/JSON) to process
            context: Processing context with country/institution/period info
            
        Returns:
            List of speech segments with speakers
        """
        if not self._validate_input(data, context):
            return []
        
        if not data or not data.strip():
            self.logger.warning("Empty text provided for speaker extraction")
            return []
        
        operation_name = f"extract_speakers_{context.country}_{context.institution_id}"
        
        with self._operation_context(operation_name, context):
            # Get patterns for this context
            patterns = self._get_patterns_for_context(context)
            
            if not patterns:
                self.logger.warning("No regex patterns available for speaker extraction")
                return []
            
            # Extract speaker matches
            speaker_matches = self._extract_speaker_matches(data, patterns)
            
            if not speaker_matches:
                self.logger.warning("No speakers found in text")
                return []
            
            # Resolve conflicts and duplicates
            speaker_matches = self._resolve_duplicate_speakers(speaker_matches)
            
            # Segment text by speakers
            segments = self._segment_text_by_speakers(data, speaker_matches)
            
            self.logger.info(f"Extracted {len(segments)} speech segments from {len(speaker_matches)} speakers")
            
            return segments
    
    def extract_speakers_only(self, raw_text: str, context: ProcessingContext) -> List[SpeakerMatch]:
        """
        Extract only speaker matches without text segmentation.
        
        Args:
            raw_text: Raw text to process
            context: Processing context
            
        Returns:
            List of speaker matches
        """
        patterns = self._get_patterns_for_context(context)
        if not patterns:
            return []
        
        speaker_matches = self._extract_speaker_matches(raw_text, patterns)
        return self._resolve_duplicate_speakers(speaker_matches)
    
    def create_speaker_entities(self, speaker_matches: List[SpeakerMatch], 
                              context: ProcessingContext) -> List[Speaker]:
        """
        Create Speaker entities from speaker matches.
        
        Args:
            speaker_matches: List of speaker matches
            context: Processing context
            
        Returns:
            List of Speaker entities
        """
        speakers = []
        
        for match in speaker_matches:
            # Create basic speaker entity
            speaker = Speaker(
                id=UUID.new(),
                name=match.speaker_name
            )
            
            # TODO: Extract additional metadata (party, role, etc.) when patterns support it
            # This would integrate with the party enum registry based on country
            
            speakers.append(speaker)
        
        return speakers
    
    def get_extraction_statistics(self, segments: List[SpeechSegment]) -> Dict[str, Any]:
        """
        Generate statistics for extraction results.
        
        Args:
            segments: List of speech segments
            
        Returns:
            Dictionary with extraction statistics
        """
        if not segments:
            return {
                'total_segments': 0,
                'unique_speakers': 0,
                'average_segment_length': 0.0,
                'total_text_length': 0,
                'speakers_frequency': {}
            }
        
        from collections import Counter
        
        # Count speakers
        speaker_names = [seg.speaker_match.speaker_name for seg in segments]
        speaker_freq = Counter(speaker_names)
        
        # Calculate text statistics
        segment_lengths = [len(seg.text_content) for seg in segments]
        total_text = sum(segment_lengths)
        
        return {
            'total_segments': len(segments),
            'unique_speakers': len(speaker_freq),
            'average_segment_length': total_text / len(segments) if segments else 0.0,
            'total_text_length': total_text,
            'speakers_frequency': dict(speaker_freq.most_common()),
            'min_segment_length': min(segment_lengths) if segment_lengths else 0,
            'max_segment_length': max(segment_lengths) if segment_lengths else 0
        }