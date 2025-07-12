from src.application.modules.fetchers.bundestag_fetcher import BundestagFetcher
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.config import APIConfig
from src.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from src.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum

# ================= Fetchers =================

def get_bundestag_fetcher():
    config = APIConfig()
    country_repo = CountryRepository()
    institution_repo = InstitutionRepository()
    country = country_repo.get_by_country_enum(CountryEnum.GERMANY)
    if not country:
        raise RuntimeError("Germany country not found in DB")
    institution = institution_repo.get_by_country_id_and_type(
        country.id, InstitutionTypeEnum.PARLIAMENT)
    if not institution:
        raise RuntimeError("Bundestag institution not found in DB")
    api = BundestagAPI(config, country, institution)
    repository = ProtocolRepository()
    return BundestagFetcher(api, repository)
