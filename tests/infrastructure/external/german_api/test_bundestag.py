import os
import pytest
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.domain.models.common.ve_metadata_plugin import MetadataPlugin
from src.config import APIConfig

@pytest.mark.integration
def test_bundestag_api_real_request():

    base_url = os.environ.get("BUNDESTAG_API_BASE_URL", "https://search.dip.bundestag.de/api")
    api_key = os.environ.get("BUNDESTAG_API_KEY", None)
    assert api_key, "API key must be set in BUNDESTAG_API_KEY env var"

    config = APIConfig()
    setattr(config, 'BASE_URL', base_url)
    setattr(config, 'API_KEY', api_key)

    country = CountryEnum.GERMANY
    institution = Institution(
        id=UUID.new(),
        country_id=UUID.new(),
        institution_type=InstitutionTypeEnum.PARLIAMENT,
        periodisation=[],
        metadata=MetadataPlugin({})
    )
    api = BundestagAPI(config, country, institution)

    protocol_spec = "20/1"
    period = None

    url = api.build_request(protocol_spec, period)
    response = api.fetch_protocol(url)
    protocol = api.parse_response(response)

    assert protocol.id is not None
    assert protocol.institution_id == institution.id
    assert protocol.protocol_text is not None
    assert protocol.date is not None
    assert protocol.extension is not None
    assert protocol.protocol_type is not None
    assert protocol.file_source is not None
    assert hasattr(protocol, "agenda") or hasattr(protocol, "_agenda")
    assert isinstance(protocol.metadata, dict)
