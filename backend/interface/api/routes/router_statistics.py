from fastapi import APIRouter, HTTPException, Depends
from backend.application.di.di_statistics import get_statistics_use_case
from backend.application.use_cases.statistics.statistics import StatisticsUseCase
from backend.interface.api.dtos.dto_statistics import AppStatisticsDTO
from backend.interface.api.mappers.mp_statistics import statistics_to_dto

statistics_router = APIRouter()

@statistics_router.get("/app_statistics", response_model=AppStatisticsDTO)
def get_app_statistics(use_case: StatisticsUseCase = Depends(get_statistics_use_case)):
    try:
        result = use_case.execute()
        return statistics_to_dto(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching statistics failed: {str(e)}")
