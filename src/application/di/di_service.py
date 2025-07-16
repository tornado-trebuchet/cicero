from src.application.modules.fetchers.germany.bundestag_fetcher import BundestagFetcher
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.application.modules.fetchers.spec import Spec
from src.config import APIConfig

# ================= Fetchers =================

def get_bundestag_fetcher(spec: Spec):
    config = APIConfig()
    api = BundestagAPI(config)
    repository = ProtocolRepository()
    return BundestagFetcher(api, repository, spec)
