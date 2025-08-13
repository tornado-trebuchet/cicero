from pydantic import BaseModel

class AppStatisticsDTO(BaseModel):
    total_countries: int
    total_institutions: int
    total_speeches: int
    total_speakers: int
    total_protocols: int
