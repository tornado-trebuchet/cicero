from dataclasses import dataclass
from backend.domain.models.common.v_common import UUID, DateTime
from domain.irepository.text.i_speech import ISpeechRepository
from domain.irepository.common.i_joint_q import IJointQRepository
from domain.irepository.context.i_institution import IInstitutionRepository
from domain.irepository.context.i_country import ICountryRepository
from backend.domain.models.common.v_enums import (
    CountryEnum,
    InstitutionTypeEnum,
    LanguageEnum,
)

@dataclass
class MetadataDict:
    country: CountryEnum
    institution: InstitutionTypeEnum
    languge_code: LanguageEnum
    date: DateTime

# TODO: add caching and graceful exceptions
class SpeechMetadata: 
    def __init__(self,          
        speech_repo: ISpeechRepository, 
        joint_repo: IJointQRepository,
        institution_repo: IInstitutionRepository,
        country_repo: ICountryRepository
    ):
        self.speech_repository = speech_repo
        self.joint_repository = joint_repo
        self.institution_repository = institution_repo
        self.country_repository = country_repo

    def get_speech_metadata(self, speech_id: UUID) -> MetadataDict:
        speech = self.speech_repository.get_by_id(speech_id)
        if not speech:
            raise ValueError(f"Speech with id {speech_id} not found")
        speech_text = self.joint_repository.get_speech_text_by_speech_id(speech_id)
        if not speech_text:
            raise ValueError(f"Speech text for speech with id {speech_id} not found")
        language_code = speech_text.language_code
        protocol = self.joint_repository.get_protocol_by_speech_id(speech.id)
        if not protocol:
            raise ValueError(f"Protocol for speech with id {speech_id} not found")
        date = protocol.date
        institution = self.institution_repository.get_by_id(protocol.institution_id)
        if not institution:
            raise ValueError(f"Institution for protocol with id {protocol.id} not found")
        country = self.country_repository.get_by_id(institution.country_id)
        if not country:
            raise ValueError(f"Country for institution with id {institution.id} not found")

        return MetadataDict(
            country=country.country,
            institution=institution.type,
            languge_code=language_code,
            date=date
        )