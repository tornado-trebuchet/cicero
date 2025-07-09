from fastapi import FastAPI, HTTPException
from .dtos.protocol import ProtocolFetchRequest, ProtocolFetchResponse
from .dtos.institution import InstitutionCreateRequest, InstitutionCreateResponse
from .dtos.country import CountryCreateRequest, CountryCreateResponse

# --- Imports for wiring up dependencies ---
from src.config import APIConfig
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.application.modules.fetchers.bundestag_fetcher import BundestagFetcher
from src.application.use_cases.uc_institution import CreateInstitutionUseCase
from src.application.use_cases.uc_country import CreateCountryUseCase

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

@app.post("/institutions/create", response_model=InstitutionCreateResponse)
def create_institution(request: InstitutionCreateRequest):
    try:
        use_case = CreateInstitutionUseCase()
        institution = use_case.execute(
            id=UUID(request.id),
            country_id=UUID(request.country_id),
            type=request.type,
            metadata=request.metadata
        )
        return InstitutionCreateResponse(success=True, message="Institution created.", institution_id=str(institution.id))
    except Exception as e:
        return InstitutionCreateResponse(success=False, message=str(e), institution_id=None)

@app.post("/countries/create", response_model=CountryCreateResponse)
def create_country(request: CountryCreateRequest):
    try:
        use_case = CreateCountryUseCase()
        country_obj = use_case.execute(
            id=UUID(request.id),
            country=request.country,
            periodisation=None,
            institutions=None,
            parties=None,
            speakers=None
        )
        return CountryCreateResponse(success=True, message="Country created.", country_id=str(country_obj.id))
    except Exception as e:
        return CountryCreateResponse(success=False, message=str(e), country_id=None)
