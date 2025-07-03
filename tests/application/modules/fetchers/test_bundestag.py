from src.application.modules.fetchers.bundestag_fetcher import BundestagFetcher
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.infrastructure.orm.base_orm import DatabaseConfig
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.config import APIConfig

def test_bundestag_fetcher_full_chain():
    # Setup in-memory database
    db_url = "sqlite:///:memory:"
    db_config = DatabaseConfig(db_url)
    db_config.create_tables()
    session = db_config.get_session()

    # Prepare real API and repository
    config = APIConfig()
    country = CountryEnum.GERMANY
    institution = Institution(
        id=UUID.new(),
        country_id=UUID.new(),
        institution_type=InstitutionTypeEnum.PARLIAMENT,
        periodisation=[],
        metadata=MetadataPlugin({})
    )
    api = BundestagAPI(config, country, institution)
    repository = ProtocolRepository(session)
    fetcher = BundestagFetcher(api, repository)

    # Use a known-valid protocol_spec
    protocol_spec = "20/6"
    period = None

    protocol = fetcher.fetch_protocol(protocol_spec, period)

    # Assert Protocol type and DB persistence
    from src.domain.models.text.a_protocol import Protocol as ProtocolDomain
    assert isinstance(protocol, ProtocolDomain)
    found = repository.get_by_id(protocol.id)
    assert found is not None
    assert found.id == protocol.id

    # Clean up
    session.close()
