from src.application.modules.fetchers.bundestag_fetcher import BundestagFetcher
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.config import APIConfig

# ================= Fetchers =================

def get_bundestag_fetcher():
    config = APIConfig()
    api = BundestagAPI(config)  # Defaults to Germany/Parliament
    repository = ProtocolRepository()
    return BundestagFetcher(api, repository)
