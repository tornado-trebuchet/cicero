#type: ignore
from fastapi import APIRouter, Depends, HTTPException

from backend.application.di.di_common import get_seed_defaults_use_case
from backend.application.di.di_service import get_bundestag_fetcher
from backend.application.modules.text_services.extractor.extractor import (
    ExtractorService,
)
from backend.application.use_cases.common.seed_defaults import SeedDefaultsUseCase
from backend.domain.models.common.v_enums import (
    CountryEnum,
    InstitutionTypeEnum,
    LanguageEnum,
    ProtocolTypeEnum,
)
from backend.interface.api.dtos.dto_common import SeedDefaultsResponseDTO
from backend.interface.api.dtos.dto_service import (
    ExtractionSpecDTO,
    ProtocolSpecDTO,
)
from backend.interface.api.mappers.mp_service import (
    dto_to_extraction_spec,
    dto_to_protocol_spec,
)
from backend.interface.api.mappers.mp_text import protocol_to_dto, speech_to_dto

develop_router = APIRouter()


@develop_router.post("/develop/seed", response_model=SeedDefaultsResponseDTO)
def seed_defaults(
    seed_defaults_use_case: SeedDefaultsUseCase = Depends(get_seed_defaults_use_case),
) -> SeedDefaultsResponseDTO:
    try:
        seed_defaults_use_case.execute()
        return SeedDefaultsResponseDTO(detail="Seeding completed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seeding failed: {str(e)}")


@develop_router.post("/develop/seed_fetch_extract", response_model=dict)
def seed_fetch_extract(
    seed_defaults_use_case: SeedDefaultsUseCase = Depends(get_seed_defaults_use_case),
):
    """
    Seeds the database, fetches protocols with default parameters, and extracts speeches from each.
    Streams results to avoid memory clogging.
    """
    try:
        # 1. Seed the database
        seed_defaults_use_case.execute()
        seed_result = "Seeding completed"

        # 2. Fetch protocol UUIDs (hardcoded default params for Bundestag)
        protocol_spec = ProtocolSpecDTO(server_base=None, endpoint_spec=None, full_link=None, params=None)
        fetcher = get_bundestag_fetcher(dto_to_protocol_spec(protocol_spec))
        protocol_ids = fetcher.fetch_list()  # List of UUIDs

        extracted_speeches = []
        protocol_details = []
        skipped_protocols = []

        for protocol_id in protocol_ids:
            # Query protocol by ID (assume fetcher or repo has get_by_id)
            protocol = fetcher._repository.get_by_id(protocol_id)
            if not protocol:
                continue
            protocol_dto = protocol_to_dto(protocol)

            # Extract speeches for each protocol
            extraction_spec = ExtractionSpecDTO(
                protocol=protocol.id.value,
                country=CountryEnum.GERMANY,
                institution=InstitutionTypeEnum.PARLIAMENT,
                language=LanguageEnum.DE,
                protocol_type=ProtocolTypeEnum.PLENARY,
                pattern_spec=None,
            )
            extractor_service = ExtractorService()
            try:
                speeches = extractor_service.extract_speeches(dto_to_extraction_spec(extraction_spec))
                speeches_dto = [speech_to_dto(s) for s in speeches]

                protocol_details.append(protocol_dto.model_dump())
                extracted_speeches.extend([s.model_dump() for s in speeches_dto])
            except ValueError as ve:
                if "already has speeches" in str(ve):
                    skipped_protocols.append({
                        "protocol_id": str(protocol.id.value),
                        "reason": str(ve)
                    })
                else:
                    raise

        return {
            "seed_result": seed_result,
            "protocols": protocol_details,
            "speeches": extracted_speeches,
            "skipped_protocols": skipped_protocols,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")
