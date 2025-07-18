from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.application.di.di_context import (
    list_countries_use_case,
    get_country_by_id_use_case,
    get_institution_by_id_use_case,
    get_country_by_enum_use_case,
    get_institutions_by_type_use_case,
    list_institutions_use_case,
    get_party_by_id_use_case,
    get_party_by_name_use_case,
    list_parties_use_case,
    get_period_by_id_use_case,
    get_periods_by_owner_id_use_case,
    get_periods_by_owner_use_case,
    get_period_by_label_use_case,
    list_periods_use_case,
    get_speaker_by_id_use_case,
    get_speakers_by_name_use_case,
)
from src.interface.api.dtos.dto_context import CountryDTO, InstitutionDTO, PartyDTO, PeriodDTO, SpeakerDTO
from src.interface.api.mappers.mp_context import institution_to_dto, country_to_dto, party_to_dto, period_to_dto, speaker_to_dto

# TODO: can be done better with filters also WTF is this DI?
context_router = APIRouter()

@context_router.get("/countries", response_model=List[CountryDTO])
def list_countries(list_countries_use_case: Any = Depends(list_countries_use_case)) -> List[CountryDTO]:
    countries = list_countries_use_case.execute()
    return [country_to_dto(country) for country in countries]

@context_router.get("/countries/{country_id}", response_model=CountryDTO)
def get_country_by_id(country_id: str, use_case: Any = Depends(get_country_by_id_use_case)) -> CountryDTO:
    country = use_case.execute(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_to_dto(country)

@context_router.get("/countries/by_enum/{country_enum}", response_model=CountryDTO)
def get_country_by_enum(country_enum: CountryEnum, use_case: Any = Depends(get_country_by_enum_use_case)) -> CountryDTO:
    country = use_case.execute(country_enum)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_to_dto(country)

@context_router.get("/institutions", response_model=List[InstitutionDTO])
def list_institutions(list_institutions_use_case: Any = Depends(list_institutions_use_case)) -> List[InstitutionDTO]:
    institutions = list_institutions_use_case.execute()
    return [institution_to_dto(inst) for inst in institutions]

@context_router.get("/institutions/{institution_id}", response_model=InstitutionDTO)
def get_institution_by_id(institution_id: str, use_case: Any = Depends(get_institution_by_id_use_case)) -> InstitutionDTO:
    institution = use_case.execute(institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution_to_dto(institution)

@context_router.get("/institutions/by_type/{institution_type}", response_model=List[InstitutionDTO])
def get_institutions_by_type(institution_type: InstitutionTypeEnum, use_case: Any = Depends(get_institutions_by_type_use_case)) -> List[InstitutionDTO]:
    institutions = use_case.execute(institution_type)
    return [institution_to_dto(inst) for inst in institutions]

@context_router.get("/parties", response_model=List[PartyDTO])
def list_parties(list_parties_use_case: Any = Depends(list_parties_use_case)) -> List[PartyDTO]:
    parties = list_parties_use_case.execute()
    return [party_to_dto(party) for party in parties]

@context_router.get("/parties/{party_id}", response_model=PartyDTO)
def get_party_by_id(party_id: str, use_case: Any = Depends(get_party_by_id_use_case)) -> PartyDTO:
    party = use_case.execute(party_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party_to_dto(party)

@context_router.get("/parties/by_name/{party_name}", response_model=PartyDTO)
def get_party_by_name(party_name: str, use_case: Any = Depends(get_party_by_name_use_case)) -> PartyDTO:
    party = use_case.execute(party_name)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party_to_dto(party)

@context_router.get("/periods", response_model=List[PeriodDTO])
def list_periods(list_periods_use_case: Any = Depends(list_periods_use_case)) -> List[PeriodDTO]:
    periods = list_periods_use_case.execute()
    return [period_to_dto(period) for period in periods]

@context_router.get("/periods/{period_id}", response_model=PeriodDTO)
def get_period_by_id(period_id: str, use_case: Any = Depends(get_period_by_id_use_case)) -> PeriodDTO:
    period = use_case.execute(period_id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    return period_to_dto(period)

@context_router.get("/periods/by_owner_id/{owner_id}", response_model=List[PeriodDTO])
def get_periods_by_owner_id(owner_id: str, use_case: Any = Depends(get_periods_by_owner_id_use_case)) -> List[PeriodDTO]:
    periods = use_case.execute(owner_id)
    return [period_to_dto(p) for p in periods]

@context_router.get("/periods/by_owner/{owner_id}/{owner_type}", response_model=List[PeriodDTO])
def get_periods_by_owner(owner_id: str, owner_type: str, use_case: Any = Depends(get_periods_by_owner_use_case)) -> List[PeriodDTO]:
    periods = use_case.execute(owner_id, owner_type)
    return [period_to_dto(p) for p in periods]

@context_router.get("/periods/by_label/{label}", response_model=PeriodDTO)
def get_period_by_label(label: str, use_case: Any = Depends(get_period_by_label_use_case)) -> PeriodDTO:
    period = use_case.execute(label)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    return period_to_dto(period)

@context_router.get("/speakers/{speaker_id}", response_model=SpeakerDTO)
def get_speaker_by_id(speaker_id: str, use_case: Any = Depends(get_speaker_by_id_use_case)) -> SpeakerDTO:
    speaker = use_case.execute(speaker_id)
    if not speaker:
        raise HTTPException(status_code=404, detail="Speaker not found")
    return speaker_to_dto(speaker)

@context_router.get("/speakers/by_name/{name}", response_model=List[SpeakerDTO])
def get_speakers_by_name(name: str, use_case: Any = Depends(get_speakers_by_name_use_case)) -> List[SpeakerDTO]:
    speakers = use_case.execute(name)
    return [speaker_to_dto(s) for s in speakers]