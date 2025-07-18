from fastapi import APIRouter, Depends, HTTPException

from src.application.di.di_common import get_seed_defaults_use_case
from src.application.di.di_service import get_bundestag_fetcher
from src.application.modules.text_services.extractor.extractor import (
    ExtractorService,
)
from src.application.use_cases.common.seed_defaults import SeedDefaultsUseCase
from src.domain.models.common.v_enums import (
    CountryEnum,
    InstitutionTypeEnum,
    LanguageEnum,
    ProtocolTypeEnum,
)
from src.interface.api.dtos.dto_common import SeedDefaultsResponseDTO
from src.interface.api.dtos.dto_service import (
    ExtractionSpecDTO,
    ProtocolSpecDTO,
)
from src.interface.api.mappers.mp_service import (
    dto_to_extraction_spec,
    dto_to_protocol_spec,
)
from src.interface.api.mappers.mp_text import protocol_to_dto, speech_to_dto

develop_router = APIRouter()


@develop_router.post("/develop/seed", response_model=SeedDefaultsResponseDTO)
def seed_defaults(
    seed_defaults_use_case: SeedDefaultsUseCase = Depends(
        get_seed_defaults_use_case
    ),
) -> SeedDefaultsResponseDTO:
    try:
        seed_defaults_use_case.execute()
        return SeedDefaultsResponseDTO(detail="Seeding completed")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Seeding failed: {str(e)}"
        )


@develop_router.post("/develop/seed_fetch_extract", response_model=dict)
def seed_fetch_extract(
    seed_defaults_use_case: SeedDefaultsUseCase = Depends(
        get_seed_defaults_use_case
    ),
):
    """
    Seeds the database, fetches a protocol with default parameters, and extracts speeches from it.
    Returns a dict with details of each step and the extracted speeches.
    """
    try:
        # 1. Seed the database
        seed_defaults_use_case.execute()
        seed_result = "Seeding completed"

        # 2. Fetch protocol (hardcoded default params for Bundestag)
        protocol_spec = ProtocolSpecDTO(
            server_base=None, endpoint_spec=None, full_link=None, params=None
        )
        fetcher = get_bundestag_fetcher(dto_to_protocol_spec(protocol_spec))
        protocol = fetcher.fetch_single()
        protocol_dto = protocol_to_dto(protocol)

        # 3. Extract speeches (using protocol info for ExtractionSpec)
        extraction_spec = ExtractionSpecDTO(
            protocol=protocol.id.value,
            country=CountryEnum.GERMANY,
            institution=InstitutionTypeEnum.PARLIAMENT,
            language=LanguageEnum.DE,
            protocol_type=ProtocolTypeEnum.PLENARY,
            pattern_spec=None,
        )
        extractor_service = ExtractorService()
        speeches = extractor_service.extract_speeches(
            dto_to_extraction_spec(extraction_spec)
        )
        speeches_dto = [speech_to_dto(s) for s in speeches]

        return {
            "seed_result": seed_result,
            "protocol": protocol_dto.model_dump(),
            "speeches": [s.model_dump() for s in speeches_dto],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Pipeline failed: {str(e)}"
        )
