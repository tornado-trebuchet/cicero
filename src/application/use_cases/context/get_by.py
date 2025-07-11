from src.domain.irepository.context.i_country import ICountryRepository
from src.domain.irepository.context.i_institution import IInstitutionRepository
from src.domain.irepository.context.i_party import IPartyRepository
from src.domain.irepository.context.i_period import IPeriodRepository
from src.domain.irepository.context.i_speaker import ISpeakerRepository
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum, OwnerTypeEnum
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_name import Name
from src.domain.models.context.v_party_name import PartyName
from src.domain.models.context.v_label import Label

class GetCountryByIdUseCase:
    def __init__(self, country_repo: ICountryRepository):
        self.country_repo = country_repo

    def execute(self, country_id: UUID):
        return self.country_repo.get_by_id(country_id)

class GetInstitutionByIdUseCase:
    def __init__(self, institution_repo: IInstitutionRepository):
        self.institution_repo = institution_repo

    def execute(self, institution_id: UUID):
        return self.institution_repo.get_by_id(institution_id)

class GetCountryByEnumUseCase:
    def __init__(self, country_repo: ICountryRepository):
        self.country_repo = country_repo

    def execute(self, country_enum: CountryEnum):
        return self.country_repo.get_by_country_enum(country_enum)

class GetInstitutionsByTypeUseCase:
    def __init__(self, institution_repo: IInstitutionRepository):
        self.institution_repo = institution_repo

    def execute(self, institution_type: InstitutionTypeEnum):
        return self.institution_repo.get_by_type(institution_type)

class GetPartyByIdUseCase:
    def __init__(self, party_repo: IPartyRepository):
        self.party_repo = party_repo

    def execute(self, party_id: UUID):
        return self.party_repo.get_by_id(party_id)

class GetPartyByNameUseCase:
    def __init__(self, party_repo: IPartyRepository):
        self.party_repo = party_repo

    def execute(self, party_name: PartyName):
        return self.party_repo.get_by_name(party_name)

class GetPeriodByIdUseCase:
    def __init__(self, period_repo: IPeriodRepository):
        self.period_repo = period_repo

    def execute(self, period_id: UUID):
        return self.period_repo.get_by_id(period_id)

class GetPeriodsByOwnerIdUseCase:
    def __init__(self, period_repo: IPeriodRepository):
        self.period_repo = period_repo

    def execute(self, owner_id: UUID):
        return self.period_repo.get_by_owner_id(owner_id)

class GetPeriodsByOwnerUseCase:
    def __init__(self, period_repo: IPeriodRepository):
        self.period_repo = period_repo

    def execute(self, owner_id: UUID, owner_type: OwnerTypeEnum):
        return self.period_repo.get_by_owner(owner_id, owner_type)

class GetPeriodByLabelUseCase:
    def __init__(self, period_repo: IPeriodRepository):
        self.period_repo = period_repo

    def execute(self, label: Label):
        return self.period_repo.get_by_label(label)

class GetSpeakerByIdUseCase:
    def __init__(self, speaker_repo: ISpeakerRepository):
        self.speaker_repo = speaker_repo

    def execute(self, speaker_id: UUID):
        return self.speaker_repo.get_by_id(speaker_id)

class GetSpeakersByNameUseCase:
    def __init__(self, speaker_repo: ISpeakerRepository):
        self.speaker_repo = speaker_repo

    def execute(self, name: Name):
        return self.speaker_repo.get_by_name(name)
