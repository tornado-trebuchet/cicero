from backend.application.use_cases.statistics.statistics import AppStatistics
from backend.interface.api.dtos.dto_statistics import AppStatisticsDTO

def statistics_to_dto(statistics: AppStatistics) -> AppStatisticsDTO:
    return AppStatisticsDTO(
        total_countries=statistics.total_countries,
        total_institutions=statistics.total_institutions,
        total_speeches=statistics.total_speeches,
        total_speakers=statistics.total_speakers,
        total_protocols=statistics.total_protocols,
    )
