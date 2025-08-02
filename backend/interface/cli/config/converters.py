"""
Configuration converters to map CLI config classes to application specification classes.
"""
from typing import List

from backend.interface.cli.config.cli_config import (
    CLIPipelineConfig,
    CLIFetcherConfig, 
    CLIExtractionConfig,
    CLIPreprocessorConfig,
    CLITopicModellerConfig,
    CLICorporaSpecConfig
)

from backend.application.pipeline.spec import PipelineSpec
from backend.application.modules.fetchers.fetcher_spec import FetcherSpec
from backend.application.modules.text_services.extractor.extractor_spec import ExtractionSpec
from backend.application.modules.text_services.preprocessor.preprocessor_spec import PreprocessorSpec
from backend.application.modules.modellers.topic_modeller.topic_spec import TopicModellerSpec
from backend.application.use_cases.common.corpora_spec import CorporaSpec

from backend.config import PipelineConfig
from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import (
    CountryEnum,
    InstitutionTypeEnum,
    LanguageEnum,
    ProtocolTypeEnum,
    PipelineType,
    PipelineStep
)
from backend.domain.models.common.a_corpora import Corpora


class ConfigConverter:
    """Converts CLI configuration objects to application specification objects"""
    
    @staticmethod
    def cli_pipeline_to_spec(cli_config: CLIPipelineConfig) -> PipelineSpec:
        """Convert CLI pipeline config to PipelineSpec"""
        
        # Convert pipeline config
        pipeline_type = PipelineType(cli_config.pipeline_type)
        steps = None
        if cli_config.steps:
            steps = [PipelineStep(step) for step in cli_config.steps]
            
        config = PipelineConfig(
            pipeline_type=pipeline_type,
            steps=steps,
            parallel_preprocessing=cli_config.parallel_preprocessing,
            batch_size=cli_config.batch_size,
            save_intermediate_results=cli_config.save_intermediate_results
        )
        
        # Convert sub-specs
        fetcher_spec = None
        if cli_config.fetcher:
            fetcher_spec = ConfigConverter.cli_fetcher_to_spec(cli_config.fetcher)
            
        extraction_spec = None
        if cli_config.extraction:
            extraction_spec = ConfigConverter.cli_extraction_to_spec(cli_config.extraction)
            
        preprocessor_specs = None
        if cli_config.preprocessor:
            preprocessor_specs = ConfigConverter.cli_preprocessor_to_specs(cli_config.preprocessor)
            
        topic_modeller_spec = None
        if cli_config.topic_modeller:
            # Topic modeller spec requires a Corpora object, which will be provided at runtime
            pass
            
        # Convert input data
        protocol_ids = None
        if cli_config.protocol_ids:
            protocol_ids = [UUID(pid) for pid in cli_config.protocol_ids]
            
        speech_ids = None
        if cli_config.speech_ids:
            speech_ids = [UUID(sid) for sid in cli_config.speech_ids]
            
        corpora_id = None
        if cli_config.corpora_id:
            corpora_id = UUID(cli_config.corpora_id)
        
        return PipelineSpec(
            config=config,
            fetcher_spec=fetcher_spec,
            extraction_spec=extraction_spec,
            preprocessor_specs=preprocessor_specs,
            topic_modeller_spec=topic_modeller_spec,
            protocol_ids=protocol_ids,
            speech_ids=speech_ids,
            corpora_id=corpora_id,
            output_corpora_label=cli_config.output_corpora_label
        )
    
    @staticmethod
    def cli_fetcher_to_spec(cli_config: CLIFetcherConfig) -> FetcherSpec:
        """Convert CLI fetcher config to FetcherSpec"""
        return FetcherSpec(
            server_base=cli_config.server_base,
            endpoint_spec=cli_config.endpoint_spec,
            endpoint_val=cli_config.endpoint_val,
            full_link=cli_config.full_link,
            params=cli_config.params
        )
    
    @staticmethod
    def cli_extraction_to_spec(cli_config: CLIExtractionConfig) -> ExtractionSpec:
        """Convert CLI extraction config to ExtractionSpec"""
        return ExtractionSpec(
            protocol=UUID(cli_config.protocol_id),
            country=CountryEnum(cli_config.country),
            institution=InstitutionTypeEnum(cli_config.institution),
            language=LanguageEnum(cli_config.language),
            protocol_type=ProtocolTypeEnum(cli_config.protocol_type),
            pattern_spec=cli_config.pattern_spec
        )
    
    @staticmethod
    def cli_preprocessor_to_specs(cli_config: CLIPreprocessorConfig) -> List[PreprocessorSpec]:
        """Convert CLI preprocessor config to list of PreprocessorSpec"""
        return [PreprocessorSpec(speech=UUID(sid)) for sid in cli_config.speech_ids]
    
    @staticmethod
    def cli_topic_modeller_to_spec(cli_config: CLITopicModellerConfig, corpora: Corpora) -> TopicModellerSpec:
        """Convert CLI topic modeller config to TopicModellerSpec"""
        return TopicModellerSpec(corpora=corpora)
    
    @staticmethod 
    def cli_corpora_spec_to_spec(cli_config: CLICorporaSpecConfig) -> CorporaSpec:
        """Convert CLI corpora spec config to CorporaSpec"""
        countries = None
        if cli_config.countries:
            countries = [UUID(cid) for cid in cli_config.countries]
            
        institutions = None
        if cli_config.institutions:
            institutions = [UUID(iid) for iid in cli_config.institutions]
            
        protocols = None
        if cli_config.protocols:
            protocols = [UUID(pid) for pid in cli_config.protocols]
            
        parties = None
        if cli_config.parties:
            parties = [UUID(pid) for pid in cli_config.parties]
            
        speakers = None
        if cli_config.speakers:
            speakers = [UUID(sid) for sid in cli_config.speakers]
            
        periods = None
        if cli_config.periods:
            periods = [UUID(pid) for pid in cli_config.periods]
        
        return CorporaSpec(
            countries=countries,
            institutions=institutions,
            protocols=protocols,
            parties=parties,
            speakers=speakers,
            periods=periods
        )
