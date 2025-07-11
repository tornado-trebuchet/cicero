from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.interface.api.dtos.dto_context import CountryDTO, InstitutionDTO
from src.domain.models.context.e_party import Party
from src.interface.api.dtos.dto_context import PartyDTO
from src.domain.models.context.e_period import Period
from src.interface.api.dtos.dto_context import PeriodDTO
from src.domain.models.context.e_speaker import Speaker
from src.interface.api.dtos.dto_context import SpeakerDTO

def country_to_dto(country: Country) -> CountryDTO:
    return CountryDTO(
        id=country.id.value,
        country=country.country,
        institutions=[i.value for i in (country.institutions or [])],
        periodisation=[p.value for p in (country.periodisation or [])],
        parties=[pa.value for pa in (country.parties or [])],
        speakers=[s.value for s in (country.speakers or [])],
    )

def institution_to_dto(institution: Institution) -> InstitutionDTO:
    metadata = institution.metadata # FIXME: Почему так то бляд? Где тебя пофиксить?
    return InstitutionDTO(
        id=institution.id.value,
        country_id=institution.country_id.value,
        type=institution.type,
        label=institution.label.value,
        protocols=[p.value for p in (institution.protocols or [])],
        periodisation=[p.value for p in (institution.periodisation or [])],
        metadata=metadata.get_properties() if metadata and hasattr(metadata, 'get_properties') else {}
    )

def party_to_dto(party: Party) -> PartyDTO:
    return PartyDTO(
        id=party.id.value,
        country_id=party.country_id.value,
        party_name=party.party_name.value,
        party_program=party.party_program.program_text if party.party_program else "",
        speakers=[s.value for s in (party.speakers or [])],
    )

def period_to_dto(period: Period) -> PeriodDTO:
    return PeriodDTO(
        id=period.id.value,
        owner_id=period.owner_id.value,
        owner_type=period.owner_type,
        label=period.label.value,
        start_date=period.start_date.value,
        end_date=period.end_date.value,
    )

def speaker_to_dto(speaker: Speaker) -> SpeakerDTO:
    return SpeakerDTO(
        id=speaker.id.value,
        country_id=speaker.country_id.value,
        name=speaker.name.value,
        speeches=[s.value for s in (speaker.speeches or [])],
        party=speaker.party.value if speaker.party is not None else None,
        role=speaker.role,
        birth_date=speaker.birth_date.value if speaker.birth_date else None,
        gender=speaker.gender if speaker.gender is not None else None,
    )