from typing import List
from backend.application.modules.text_services.extractor.extractor_spec import ExtractionSpec
from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_metadata_plugin import MetadataPlugin
from backend.domain.models.context.e_speaker import Speaker
from backend.domain.models.context.v_name import Name
from backend.domain.models.text.a_speech import Speech
from backend.domain.models.text.a_speech_text import SpeechText
from backend.domain.models.text.e_text_raw import RawText
from backend.domain.models.text.e_speech_metrics_plugin import MetricsPlugin
from backend.domain.services.text.extractor.serv_extractor import ExtractSpeakersFromProtocol
from backend.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
from backend.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from backend.infrastructure.repository.pgsql.context.rep_speaker import SpeakerRepository
from backend.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from backend.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
from backend.infrastructure.repository.pgsql.text.rep_speech_text import SpeechTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository

import logging
logger = logging.getLogger(__name__)

# TODO: inject repositories in DI, depend on contracts 
# FIXME:
# 3) Parties are not extracted
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

        logger.info(f"Extracting speeches from protocol {protocol.id}")   
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

            # Create SpeechText aggregate with proper links
            speech_text_entity = SpeechText(
                id=speech_text_id,
                speech_id=speech_id,  # Links to Speech
                raw_text=raw_text_id,  # Links to RawText
                language_code=spec.language,
            )

            # Create Speech entity
            speech_entity = Speech(
                id=speech_id,
                protocol_id=spec.protocol,
                speaker_id=speaker_entity.id,
                protocol_order=protocol_order,
                text=speech_text_id,
                metadata=(MetadataPlugin(speech_dto.metadata) if speech_dto.metadata else None),
                metrics=(MetricsPlugin(**speech_dto.metrics) if speech_dto.metrics else None),
            )

            # Create RawText entity linked to SpeechText
            raw_text_entity = RawText(
                id=raw_text_id,
                speech_text_id=speech_text_id,  # Links to SpeechText
                text=speech_dto.raw_text.text,
            )

            # Add all three entities in a single transaction
            self.joint_q_repo.add_speech_speech_text_and_raw_text(
                speech=speech_entity,
                speech_text=speech_text_entity,
                raw_text=raw_text_entity,
            )

            # Update relationships
            if speaker_entity.speeches is None:
                speaker_entity.speeches = []
            speaker_entity.speeches.append(speech_id)
            self.speaker_repo.update(speaker_entity)

            # Update protocol speeches collection
            protocol.add_speech(speech_id)
            self.protocol_repo.update(protocol)
            speeches.append(speech_entity)
            protocol_order += 1
            
        logger.info(f"Extracted {len(speeches)} speeches from protocol {protocol.id}")
        return speeches
