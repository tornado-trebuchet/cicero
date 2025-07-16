from fastapi import APIRouter, HTTPException
from src.interface.api.mappers.mp_text import protocol_to_dto
from src.interface.api.dtos.dto_text import ProtocolDTO
from src.application.di.di_service import get_bundestag_fetcher
from src.interface.api.dtos.dto_service import ProtocolSpecDTO
from src.interface.api.mappers.mp_service import dto_to_protocol_spec

service_router = APIRouter()

@service_router.post("/service/fetcher/bundestag", response_model=ProtocolDTO)
def fetch_bundestag_protocol(protocol_spec: ProtocolSpecDTO):
    try:
        spec = dto_to_protocol_spec(protocol_spec)
        fetcher = get_bundestag_fetcher(spec)
        protocol = fetcher.fetch_single()
        return protocol_to_dto(protocol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching protocol failed: {str(e)}")