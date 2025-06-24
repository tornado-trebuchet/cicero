"""
Utility module for loading regex patterns from files and supplying them to the database.
Supports various file formats and pattern management operations.
"""
import json
import csv
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

# Optional yaml support
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None

from src.domain.models.e_regex_pattern import RegexPattern
from src.domain.models.v_common import UUID
from src.domain.models.v_enums import CountryEnum
from src.domain.irepository.i_regex_pattern import IRegexPatternRepository


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
    """
    Utility class for loading regex patterns from files.
    
    Supports:
    - JSON files with pattern definitions
    - CSV files with pattern data
    - YAML files with structured patterns
    - Plain text files with one pattern per line
    """
    
    def __init__(self, repository: Optional[IRegexPatternRepository] = None):
        """Initialize the regex file loader."""
        self._repository = repository
        self._country_mapping = self._initialize_country_mapping()
    
    def _initialize_country_mapping(self) -> Dict[str, CountryEnum]:
        """Initialize mapping from string identifiers to CountryEnum."""
        return {
            'germany': CountryEnum.GERMANY,
            'de': CountryEnum.GERMANY,
            'deutschland': CountryEnum.GERMANY,
            'france': CountryEnum.FRANCE,
            'fr': CountryEnum.FRANCE,
            'france': CountryEnum.FRANCE,
        }
    
    def set_repository(self, repository: IRegexPatternRepository) -> None:
        """Set the regex pattern repository."""
        self._repository = repository
    
    def load_from_json(self, file_path: Union[str, Path]) -> List[PatternFileEntry]:
        """
        Load regex patterns from JSON file.
        
        Expected JSON format:
        {
            "patterns": [
                {
                    "pattern": "regex_pattern_here",
                    "description": "Description of pattern",
                    "country": "germany",
                    "institution": "bundestag",
                    "period": "19th_period",
                    "version": 1,
                    "is_active": true
                }
            ]
        }
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of pattern file entries
        """
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
    
    def load_from_csv(self, file_path: Union[str, Path]) -> List[PatternFileEntry]:
        """
        Load regex patterns from CSV file.
        
        Expected CSV columns: pattern, description, country, institution, period, version, is_active
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of pattern file entries
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        try:
            patterns = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    pattern_entry = PatternFileEntry(
                        pattern=row['pattern'],
                        description=row.get('description'),
                        country=row.get('country'),
                        institution=row.get('institution'),
                        period=row.get('period'),
                        version=int(row.get('version', 1)),
                        is_active=row.get('is_active', 'true').lower() == 'true'
                    )
                    patterns.append(pattern_entry)
            
            return patterns
            
        except Exception as e:
            raise ValueError(f"Error loading CSV file {file_path}: {str(e)}")
    
    def load_from_yaml(self, file_path: Union[str, Path]) -> List[PatternFileEntry]:
        """
        Load regex patterns from YAML file.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            List of pattern file entries
        """
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is not installed. Install with: pip install PyYAML")
            
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if yaml is not None:
                    data = yaml.safe_load(f)
                else:
                    raise ImportError("PyYAML is not available")
            
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
            raise ValueError(f"Error loading YAML file {file_path}: {str(e)}")
    
    def load_from_text(self, file_path: Union[str, Path], 
                      default_country: Optional[str] = None,
                      default_institution: Optional[str] = None) -> List[PatternFileEntry]:
        """
        Load regex patterns from plain text file (one pattern per line).
        
        Args:
            file_path: Path to text file
            default_country: Default country for all patterns
            default_institution: Default institution for all patterns
            
        Returns:
            List of pattern file entries
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Text file not found: {file_path}")
        
        try:
            patterns = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        pattern_entry = PatternFileEntry(
                            pattern=line,
                            description=f"Pattern from {file_path.name} line {line_no}",
                            country=default_country,
                            institution=default_institution
                        )
                        patterns.append(pattern_entry)
            
            return patterns
            
        except Exception as e:
            raise ValueError(f"Error loading text file {file_path}: {str(e)}")
    
    def validate_patterns(self, patterns: List[PatternFileEntry]) -> List[PatternFileEntry]:
        """
        Validate regex patterns for syntax errors.
        
        Args:
            patterns: List of pattern entries to validate
            
        Returns:
            List of valid pattern entries
        """
        valid_patterns = []
        
        for i, entry in enumerate(patterns):
            try:
                # Test regex compilation
                re.compile(entry.pattern)
                valid_patterns.append(entry)
                
            except re.error as e:
                print(f"Warning: Invalid regex pattern at index {i}: {entry.pattern}")
                print(f"Error: {str(e)}")
                continue
        
        return valid_patterns
    
    def convert_to_domain_entities(self, patterns: List[PatternFileEntry], 
                                  default_country_id: UUID,
                                  default_institution_id: UUID) -> List[RegexPattern]:
        """
        Convert file entries to domain entities.
        
        Args:
            patterns: List of pattern file entries
            default_country_id: Default country UUID
            default_institution_id: Default institution UUID
            
        Returns:
            List of RegexPattern domain entities
        """
        domain_patterns = []
        
        for entry in patterns:
            # Create RegexPattern entity
            regex_pattern = RegexPattern(
                id=UUID.new(),
                country=default_country_id,  # In real implementation, would map from entry.country
                institution=default_institution_id,  # In real implementation, would map from entry.institution
                pattern=entry.pattern,
                is_active=entry.is_active,
                description=entry.description,
                version=entry.version
            )
            
            domain_patterns.append(regex_pattern)
        
        return domain_patterns
    
    def load_and_save_to_repository(self, file_path: Union[str, Path],
                                   country_id: UUID,
                                   institution_id: UUID,
                                   file_type: str = 'auto') -> int:
        """
        Load patterns from file and save them to repository.
        
        Args:
            file_path: Path to pattern file
            country_id: Country UUID
            institution_id: Institution UUID
            file_type: File type ('json', 'csv', 'yaml', 'text', 'auto')
            
        Returns:
            Number of patterns successfully saved
        """
        if not self._repository:
            raise ValueError("No repository configured")
        
        file_path = Path(file_path)
        
        # Auto-detect file type if needed
        if file_type == 'auto':
            file_type = self._detect_file_type(file_path)
        
        # Load patterns based on file type
        if file_type == 'json':
            patterns = self.load_from_json(file_path)
        elif file_type == 'csv':
            patterns = self.load_from_csv(file_path)
        elif file_type == 'yaml':
            patterns = self.load_from_yaml(file_path)
        elif file_type == 'text':
            patterns = self.load_from_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Validate patterns
        valid_patterns = self.validate_patterns(patterns)
        
        # Convert to domain entities
        domain_patterns = self.convert_to_domain_entities(
            valid_patterns, country_id, institution_id
        )
        
        # Save to repository
        saved_count = 0
        for pattern in domain_patterns:
            try:
                self._repository.add(pattern)
                saved_count += 1
            except Exception as e:
                print(f"Warning: Failed to save pattern {pattern.pattern}: {str(e)}")
        
        return saved_count
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detect file type based on extension."""
        extension = file_path.suffix.lower()
        
        if extension == '.json':
            return 'json'
        elif extension == '.csv':
            return 'csv'
        elif extension in ['.yaml', '.yml']:
            return 'yaml'
        elif extension == '.txt':
            return 'text'
        else:
            # Default to text
            return 'text'
    
    def export_patterns_to_file(self, patterns: List[RegexPattern], 
                               file_path: Union[str, Path],
                               file_type: str = 'json') -> None:
        """
        Export regex patterns to file.
        
        Args:
            patterns: List of RegexPattern entities
            file_path: Output file path
            file_type: Output file type ('json', 'csv', 'yaml')
        """
        file_path = Path(file_path)
        
        if file_type == 'json':
            self._export_to_json(patterns, file_path)
        elif file_type == 'csv':
            self._export_to_csv(patterns, file_path)
        elif file_type == 'yaml':
            self._export_to_yaml(patterns, file_path)
        else:
            raise ValueError(f"Unsupported export file type: {file_type}")
    
    def _export_to_json(self, patterns: List[RegexPattern], file_path: Path) -> None:
        """Export patterns to JSON file."""
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
    
    def _export_to_csv(self, patterns: List[RegexPattern], file_path: Path) -> None:
        """Export patterns to CSV file."""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['pattern', 'description', 'version', 'is_active', 
                           'country_id', 'institution_id', 'period_id'])
            
            # Data
            for p in patterns:
                writer.writerow([
                    p.pattern,
                    p.description or '',
                    p.version or 1,
                    p.is_active,
                    str(p.country),
                    str(p.institution),
                    str(p.period) if p.period else ''
                ])
    
    def _export_to_yaml(self, patterns: List[RegexPattern], file_path: Path) -> None:
        """Export patterns to YAML file."""
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
            if yaml is not None:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            else:
                raise ImportError("PyYAML is not available")