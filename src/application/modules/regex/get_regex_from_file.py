from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import json
import re
from pathlib import Path
from src.domain.models.e_regex_pattern import RegexPattern
from src.domain.models.v_common import UUID
from src.domain.models.v_enums import CountryEnum
from src.domain.irepository.i_regex_pattern import IRegexPatternRepository

#what the fuck is this?!!
@dataclass
class PatternFileEntry:
    """Structure for regex pattern file entries."""
    pattern: str
    description: Optional[str] = None
    country: Optional[str] = None
    institution: Optional[str] = None
    period: Optional[str] = None
    version: Optional[int] = None
    is_active: bool = True
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class RegexFileLoader:
    
    def __init__(self, repository: Optional[IRegexPatternRepository] = None):
        self._repository = repository
        self._country_mapping = self._initialize_country_mapping()
    
    def _initialize_country_mapping(self) -> Dict[str, CountryEnum]:
        return {
            'de': CountryEnum.GERMANY,
            'fr': CountryEnum.FRANCE,
        }
    
    def set_repository(self, repository: IRegexPatternRepository) -> None:
        self._repository = repository
    
    def load_from_json(self, file_path: Union[str, Path]) -> List[PatternFileEntry]:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            patterns = []
            pattern_list = data.get('patterns', [])
            
            for entry in pattern_list:
                pattern_entry = PatternFileEntry(
                    pattern=entry['pattern'],
                    description=entry.get('description'),
                    country=entry.get('country'),
                    institution=entry.get('institution'),
                    period=entry.get('period'),
                    version=entry.get('version', 1),
                    is_active=entry.get('is_active', True),
                    metadata=entry.get('metadata', {})
                )
                patterns.append(pattern_entry)
            
            return patterns
            
        except Exception as e:
            raise ValueError(f"Error loading JSON file {file_path}: {str(e)}")
    
    def validate_patterns(self, patterns: List[PatternFileEntry]) -> List[PatternFileEntry]:
        valid_patterns = []
        
        for i, entry in enumerate(patterns):
            try:
                re.compile(entry.pattern)
                valid_patterns.append(entry)
                
            except re.error as e:
                print(f"Warning: Invalid regex pattern at index {i}: {entry.pattern}")
                print(f"Error: {str(e)}")
                continue
        
        return valid_patterns
    
    def convert_to_domain_entities(self, patterns: List[PatternFileEntry]) -> List[RegexPattern]:
        domain_patterns = []
        
        for entry in patterns:
            # Create RegexPattern entity
            regex_pattern = RegexPattern(
                id=UUID.new(),
                country= #pull from repo
                institution= #pull from repo
                pattern=entry.pattern,
                is_active=entry.is_active,
                description=entry.description,
                version=entry.version
            )
            
            domain_patterns.append(regex_pattern)
        
        return domain_patterns
    
    def load_and_save_to_repository(self, file_path: Union[str, Path],file_type: str = 'auto') -> int:
        if not self._repository:
            raise ValueError("No repository configured")
        
        file_path = Path(file_path)
        
        
        patterns = self.load_from_json(file_path)
        valid_patterns = self.validate_patterns(patterns)
        domain_patterns = self.convert_to_domain_entities(valid_patterns)
        saved_count = 0
        for pattern in domain_patterns:
            try:
                self._repository.add(pattern)
                saved_count += 1
            except Exception as e:
                print(f"Warning: Failed to save pattern {pattern.pattern}: {str(e)}")
        
        return saved_count
    
    def export_patterns_to_file(self, patterns: List[RegexPattern], 
                               file_path: Union[str, Path],
                               file_type: str = 'json') -> None:
        file_path = Path(file_path)
        
        if file_type == 'json':
            self._export_to_json(patterns, file_path)
        else:
            raise ValueError(f"Unsupported export file type: {file_type}")
    
    def _export_to_json(self, patterns: List[RegexPattern], file_path: Path) -> None:
        data = {
            'patterns': [
                {
                    'pattern': p.pattern,
                    'description': p.description,
                    'version': p.version,
                    'is_active': p.is_active,
                    'country_id': str(p.country),
                    'institution_id': str(p.institution),
                    'period_id': str(p.period) if p.period else None
                }
                for p in patterns
            ]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)