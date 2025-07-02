from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.config import APIConfig

def test_bundestag_api_real_request():
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

    protocol_spec = "20/6"
    period = None

    url = api.build_request(protocol_spec, period)
    response = api.fetch_protocol(url)
    protocol = api.parse_response(response)

    # Assert Protocol type and all required fields
    from src.domain.models.text.a_protocol import Protocol
    from src.domain.models.text.v_protocol_text import ProtocolText
    from src.domain.models.common.v_common import DateTime, HttpUrl
    from src.domain.models.common.v_enums import ProtocolTypeEnum, ExtensionEnum
    from src.domain.models.context.v_period import Period

    assert isinstance(protocol, Protocol)
    assert isinstance(protocol.id, UUID)
    assert protocol.id is not None
    assert isinstance(protocol.institution_id, UUID)
    assert protocol.institution_id == institution.id
    assert protocol.extension is not None and isinstance(protocol.extension, ExtensionEnum)
    assert protocol.protocol_type is not None and isinstance(protocol.protocol_type, ProtocolTypeEnum)
    assert protocol.date is not None and isinstance(protocol.date, DateTime)
    assert protocol.protocol_text is not None and isinstance(protocol.protocol_text, ProtocolText)
    assert protocol.metadata is not None and isinstance(protocol.metadata, dict)
    # Optional fields
    if protocol.file_source is not None:
        assert isinstance(protocol.file_source, HttpUrl)
    if protocol.period is not None:
        assert isinstance(protocol.period, Period)
    if hasattr(protocol, "_agenda") and protocol._agenda is not None:
        from src.domain.models.text.v_protocol_agenda import Agenda
        assert isinstance(protocol._agenda, Agenda)

    print(f"protocol.id: {protocol.id}")
    print(f"protocol.date: {protocol.date}")
    print(f"protocol.protocol_type: {protocol.protocol_type}")
    print(f"protocol.protocol_text (first 90): {str(protocol.protocol_text)[:90]}")
    print(f"protocol.file_source: {protocol.file_source}")
