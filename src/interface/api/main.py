from fastapi import FastAPI, HTTPException
from .dtos.protocol import ProtocolFetchRequest, ProtocolFetchResponse

# --- Imports for wiring up dependencies ---
from src.config import APIConfig
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.application.modules.fetchers.bundestag_fetcher import BundestagFetcher

app = FastAPI()

@app.post("/protocols/fetch", response_model=ProtocolFetchResponse)
def fetch_and_store_protocol(request: ProtocolFetchRequest):
    try:
        # --- Set up config and domain objects (using demo UUIDs) ---
        country = Country(id=UUID.new(), country=CountryEnum.GERMANY)
        institution = Institution(id=UUID.new(), country_id=UUID.new(), type=InstitutionTypeEnum.PARLIAMENT)
        
        # --- Instantiate API, repository, and fetcher ---
        config = APIConfig()
        api = BundestagAPI(config, country, institution)
        repository = ProtocolRepository()
        fetcher = BundestagFetcher(api, repository)

        # --- Fetch and store protocol ---
        protocol = fetcher.fetch_protocol(request.protocol_id)
        return ProtocolFetchResponse(success=True, message="Protocol fetched and stored.", protocol_id=str(protocol.id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
