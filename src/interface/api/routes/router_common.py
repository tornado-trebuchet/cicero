from fastapi import APIRouter, Depends, HTTPException
from src.application.di.di_common import get_seed_defaults_use_case
from src.application.use_cases.common.seed_defaults import SeedDefaultsUseCase
from src.interface.api.dtos.dto_common import SeedDefaultsResponseDTO
from src.interface.api.mappers.mp_text import protocol_to_dto
from src.interface.api.dtos.dto_text import ProtocolDTO
from src.application.di.di_service import get_bundestag_fetcher
from src.application.modules.fetchers.bundestag_fetcher import BundestagFetcher

common_router = APIRouter()

@common_router.post("/common/seed", response_model=SeedDefaultsResponseDTO)
def seed_defaults(seed_defaults_use_case: SeedDefaultsUseCase = Depends(get_seed_defaults_use_case)) -> SeedDefaultsResponseDTO:
    try:
        seed_defaults_use_case.execute()
        return SeedDefaultsResponseDTO(detail="Seeding completed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seeding failed: {str(e)}")

# FIXME: GETS THE ID OF A PROTOCOL REFACTOR THIS AND MAKE VARIABLE CLEAR ALSO IT"S A POST
@common_router.get("/common/bundestag/protocol", response_model=ProtocolDTO)
def fetch_bundestag_protocol(protocol_spec: str, fetcher: BundestagFetcher = Depends(get_bundestag_fetcher)):
    try:
        protocol = fetcher.fetch_protocol(protocol_spec)
        return protocol_to_dto(protocol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching protocol failed: {str(e)}")
