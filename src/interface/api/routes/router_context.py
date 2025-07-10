from fastapi import APIRouter, Depends, HTTPException
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.application.di.di_context import (
    get_list_countries_use_case,
    get_country_by_id_use_case,
    get_institution_by_id_use_case,
    get_country_by_enum_use_case,
    get_institutions_by_type_use_case,
    get_list_institutions_use_case,
)
from typing import List, Any
from src.interface.api.dtos.dto_context import CountryDTO, InstitutionDTO
from src.interface.api.mappers.mp_context import institution_to_dto, country_to_dto

context_router = APIRouter()

@context_router.get("/countries", response_model=List[CountryDTO])
def list_countries(list_countries_use_case: Any = Depends(get_list_countries_use_case)) -> List[CountryDTO]:
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
def list_institutions(list_institutions_use_case: Any = Depends(get_list_institutions_use_case)) -> List[InstitutionDTO]:
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


