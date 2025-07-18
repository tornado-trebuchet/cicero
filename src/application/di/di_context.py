# Repository imports
from src.application.use_cases.context.delete import (
    DeleteCountryUseCase,
    DeleteInstitutionUseCase,
    DeletePartyUseCase,
    DeletePeriodUseCase,
    DeleteSpeakerUseCase,
)
from src.application.use_cases.context.get_by import (
    GetCountryByEnumUseCase,
    GetCountryByIdUseCase,
    GetInstitutionByIdUseCase,
    GetInstitutionsByTypeUseCase,
    GetPartyByIdUseCase,
    GetPartyByNameUseCase,
    GetPeriodByIdUseCase,
    GetPeriodByLabelUseCase,
    GetPeriodsByOwnerIdUseCase,
    GetPeriodsByOwnerUseCase,
    GetSpeakerByIdUseCase,
    GetSpeakersByNameUseCase,
)

# Use case imports
from src.application.use_cases.context.list import (
    ListCountriesUseCase,
    ListInstitutionsUseCase,
    ListPartiesUseCase,
    ListPeriodsUseCase,
)
from src.infrastructure.repository.pgsql.context.rep_country import (
    CountryRepository,
)
from src.infrastructure.repository.pgsql.context.rep_institution import (
    InstitutionRepository,
)
from src.infrastructure.repository.pgsql.context.rep_party import (
    PartyRepository,
)
from src.infrastructure.repository.pgsql.context.rep_period import (
    PeriodRepository,
)
from src.infrastructure.repository.pgsql.context.rep_speaker import (
    SpeakerRepository,
)

# ============= Repository Injection ==============


def get_country_repository():
    return CountryRepository()


def get_institution_repository():
    return InstitutionRepository()


def get_party_repository():
    return PartyRepository()


def get_period_repository():
    return PeriodRepository()


def get_speaker_repository():
    return SpeakerRepository()


# ============= UseCase Injection ==============


def list_countries_use_case():
    return ListCountriesUseCase(get_country_repository())


def get_country_by_id_use_case():
    return GetCountryByIdUseCase(get_country_repository())


def get_institution_by_id_use_case():
    return GetInstitutionByIdUseCase(get_institution_repository())


def get_country_by_enum_use_case():
    return GetCountryByEnumUseCase(get_country_repository())


def get_institutions_by_type_use_case():
    return GetInstitutionsByTypeUseCase(get_institution_repository())


def list_institutions_use_case():
    return ListInstitutionsUseCase(get_institution_repository())


def get_party_by_id_use_case():
    return GetPartyByIdUseCase(get_party_repository())


def get_party_by_name_use_case():
    return GetPartyByNameUseCase(get_party_repository())


def list_parties_use_case():
    return ListPartiesUseCase(get_party_repository())


def get_period_by_id_use_case():
    return GetPeriodByIdUseCase(get_period_repository())


def get_periods_by_owner_id_use_case():
    return GetPeriodsByOwnerIdUseCase(get_period_repository())


def get_periods_by_owner_use_case():
    return GetPeriodsByOwnerUseCase(get_period_repository())


def get_period_by_label_use_case():
    return GetPeriodByLabelUseCase(get_period_repository())


def list_periods_use_case():
    return ListPeriodsUseCase(get_period_repository())


def get_speaker_by_id_use_case():
    return GetSpeakerByIdUseCase(get_speaker_repository())


def get_speakers_by_name_use_case():
    return GetSpeakersByNameUseCase(get_speaker_repository())


def delete_country_use_case():
    return DeleteCountryUseCase(get_country_repository())


def delete_institution_use_case():
    return DeleteInstitutionUseCase(get_institution_repository())


def delete_party_use_case():
    return DeletePartyUseCase(get_party_repository())


def delete_period_use_case():
    return DeletePeriodUseCase(get_period_repository())


def delete_speaker_use_case():
    return DeleteSpeakerUseCase(get_speaker_repository())
