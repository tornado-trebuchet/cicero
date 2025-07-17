from typing import List
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.v_name import Name
from src.domain.models.text.e_text_raw import RawText
from src.domain.models.common.v_common import UUID
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.domain.models.text.v_speech_metrics_plugin import MetricsPlugin
from src.infrastructure.repository.pgsql.context.rep_speaker import SpeakerRepository
from src.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from src.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository
from src.infrastructure.repository.pgsql.text.rep_speech_text import SpeechTextRepository
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
from src.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
from src.application.modules.text_services.extractor.extractor_spec import ExtractionSpec
from src.domain.services.text.extractor.serv_extractor import ExtractSpeakersFromProtocol

# TODO: MB inject repositories in DI, would be cool?
class ExtractorService:
    def __init__(self):
        self.protocol_repo = ProtocolRepository()
        self.speech_repo = SpeechRepository()
        self.speaker_repo = SpeakerRepository()
        self.country_repo = CountryRepository()
        self.raw_text_repo = RawTextRepository()
        self.speech_text_repo = SpeechTextRepository()
        self.joint_q_repo = JointQRepository()

    def extract_speeches(self, spec: ExtractionSpec) -> List[Speech]:
        protocol = self.protocol_repo.get_by_id(spec.protocol)
        if not protocol:
            raise ValueError(f"Protocol with id {spec.protocol} not found.")
        
        existing_speeches = self.speech_repo.get_by_protocol_id(spec.protocol)
        if existing_speeches:
            raise ValueError(f"Protocol {spec.protocol} already has speeches. Extraction aborted.")
        
        extractor = ExtractSpeakersFromProtocol(protocol, spec)
        pattern_cls = extractor.pick_pattern()
        if not pattern_cls:
            raise ValueError("No matching regex pattern found for provided spec.")
        
        # Workhorse if you've lost it 
        speeches_dto = extractor.process(protocol, pattern_cls)
        protocol_order = 1
        
        speeches: List[Speech] = []
        for speech_dto in speeches_dto:
            speaker_name = speech_dto.speaker.name
            
            # Get country_id from protocol's institution
            country = self.joint_q_repo.get_country_by_institution_id(protocol.institution_id)
            if not country:
                raise ValueError(f"Country not found for protocol institution {protocol.institution_id}")
            country_id = country.id
            
            # Check for existing speaker or create new one
            speaker_entity = self.speaker_repo.get_by_country_id_and_name(country_id, Name(speaker_name))
            if not speaker_entity:
                speaker_id = UUID.new()
                speaker_entity = Speaker(
                    id=speaker_id,
                    country_id=country_id,
                    name=Name(speaker_name),
                    speeches=[],
                )
                self.speaker_repo.add(speaker_entity)
                
                # Add new speaker to country's speakers collection
                if country.speakers is None:
                    country.speakers = []
                country.add_speaker(speaker_id)
                self.country_repo.update(country)
            
            # Generate all UUIDs upfront
            speech_id = UUID.new()
            speech_text_id = UUID.new()
            raw_text_id = UUID.new()

            # Create Speech entity first
            speech_entity = Speech(
                id=speech_id,
                protocol_id=spec.protocol,
                speaker_id=speaker_entity.id,
                protocol_order=protocol_order,
                text=None,  # Will be set after SpeechText is created
                metadata=MetadataPlugin(speech_dto.metadata) if speech_dto.metadata else None,
                metrics=MetricsPlugin(**speech_dto.metrics) if speech_dto.metrics else None
            )
            self.speech_repo.add(speech_entity)

            # Create SpeechText aggregate with proper links
            speech_text_entity = SpeechText(
                id=speech_text_id,
                speech_id=speech_id,  # Links to Speech
                raw_text=raw_text_id,  # Links to RawText
                language_code=spec.language,
            )
            self.speech_text_repo.add(speech_text_entity)

            # Create RawText entity linked to SpeechText
            raw_text_entity = RawText(
                id=raw_text_id,
                speech_id=speech_text_id,  # Links to SpeechText
                text=speech_dto.raw_text.text
            )
            self.raw_text_repo.add(raw_text_entity)

            # Update Speech entity to link SpeechText aggregate
            speech_entity.text = speech_text_entity
            self.speech_repo.update(speech_entity)
            speeches.append(speech_entity)
            
            # Update bidirectional relationships
            if speaker_entity.speeches is None:
                speaker_entity.speeches = []
            speaker_entity.speeches.append(speech_id)
            self.speaker_repo.update(speaker_entity)
            
            # Update protocol speeches collection
            protocol.add_speech(speech_id)
            self.protocol_repo.update(protocol)
            
            protocol_order += 1
        
        return speeches
