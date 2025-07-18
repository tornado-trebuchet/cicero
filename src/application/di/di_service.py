from src.application.modules.fetchers.fetcher_spec import FetcherSpec
from src.application.modules.fetchers.germany.bundestag_fetcher import (
    BundestagFetcher,
)
from src.config import APIConfig
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import (
    ProtocolRepository,
)

# ================= Fetchers =================


def get_bundestag_fetcher(spec: FetcherSpec):
    config = APIConfig()
    api = BundestagAPI(config)
    repository = ProtocolRepository()
    return BundestagFetcher(api, repository, spec)
