from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.interface.api.dtos.dto_context import CountryDTO, InstitutionDTO


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
