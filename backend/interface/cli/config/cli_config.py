from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path
import yaml
import json

@dataclass
class CLIFetcherConfig:
    """Configuration for fetcher operations"""
    server_base: Optional[str] = None
    endpoint_spec: Optional[str] = None
    endpoint_val: Optional[str] = None
    full_link: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    

@dataclass 
class CLIExtractionConfig:
    """Configuration for speech extraction"""
    protocol_id: str
    country: str  # CountryEnum name
    institution: str  # InstitutionTypeEnum name  
    language: str  # LanguageEnum name
    protocol_type: str  # ProtocolTypeEnum name
    pattern_spec: Optional[Any] = None


@dataclass
class CLIPreprocessorConfig:
    """Configuration for text preprocessing"""
    speech_ids: List[str]
    

@dataclass
class CLITopicModellerConfig:
    """Configuration for topic modeling"""
    corpora_id: str


@dataclass
class CLICorporaSpecConfig:
    """Configuration for corpora specification"""
    countries: Optional[List[str]] = None
    institutions: Optional[List[str]] = None
    protocols: Optional[List[str]] = None
    parties: Optional[List[str]] = None
    speakers: Optional[List[str]] = None
    periods: Optional[List[str]] = None
    label: Optional[str] = None


@dataclass
class CLIPipelineConfig:
    """Configuration for pipeline execution"""
    pipeline_type: str  # PipelineType name
    steps: Optional[List[str]] = None  # PipelineStep names for custom pipelines
    parallel_preprocessing: bool = False
    batch_size: Optional[int] = None
    save_intermediate_results: bool = True
    
    # Step configurations
    fetcher: Optional[CLIFetcherConfig] = None
    extraction: Optional[CLIExtractionConfig] = None
    preprocessor: Optional[CLIPreprocessorConfig] = None
    topic_modeller: Optional[CLITopicModellerConfig] = None
    
    # Input data for partial pipelines
    protocol_ids: Optional[List[str]] = None
    speech_ids: Optional[List[str]] = None
    corpora_id: Optional[str] = None
    
    # Output configuration  
    output_corpora_label: Optional[str] = None


class ConfigLoader:
    """Utility class for loading CLI configurations from files"""
    
    @staticmethod
    def load_pipeline_config(file_path: Path) -> CLIPipelineConfig:
        """Load pipeline configuration from YAML or JSON file"""
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
        return ConfigLoader._dict_to_pipeline_config(data)
    
    @staticmethod
    def load_corpora_spec_config(file_path: Path) -> CLICorporaSpecConfig:
        """Load corpora spec configuration from YAML or JSON file"""
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
        return CLICorporaSpecConfig(**data)
    
    @staticmethod
    def _dict_to_pipeline_config(data: Dict[str, Any]) -> CLIPipelineConfig:
        """Convert dictionary to CLIPipelineConfig"""
        # Extract nested configs
        fetcher_data = data.get('fetcher')
        fetcher = CLIFetcherConfig(**fetcher_data) if fetcher_data else None
        
        extraction_data = data.get('extraction')
        extraction = CLIExtractionConfig(**extraction_data) if extraction_data else None
        
        preprocessor_data = data.get('preprocessor')
        preprocessor = CLIPreprocessorConfig(**preprocessor_data) if preprocessor_data else None
        
        topic_modeller_data = data.get('topic_modeller')
        topic_modeller = CLITopicModellerConfig(**topic_modeller_data) if topic_modeller_data else None
        
        # Build main config
        config_data = {k: v for k, v in data.items() if k not in ['fetcher', 'extraction', 'preprocessor', 'topic_modeller']}
        
        return CLIPipelineConfig(
            **config_data,
            fetcher=fetcher,
            extraction=extraction,
            preprocessor=preprocessor,
            topic_modeller=topic_modeller
        )
