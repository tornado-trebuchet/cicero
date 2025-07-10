from fastapi import APIRouter, Depends, HTTPException
from src.application.di.di_common import get_seed_defaults_use_case
from src.application.use_cases.common.seed_defaults import SeedDefaultsUseCase
from src.interface.api.dtos.dto_common import SeedDefaultsResponseDTO

common_router = APIRouter()

@common_router.post("/common/seed", response_model=SeedDefaultsResponseDTO)
def seed_defaults(seed_defaults_use_case: SeedDefaultsUseCase = Depends(get_seed_defaults_use_case)) -> SeedDefaultsResponseDTO:
    try:
        seed_defaults_use_case.execute()
        return SeedDefaultsResponseDTO(detail="Seeding completed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seeding failed: {str(e)}")
