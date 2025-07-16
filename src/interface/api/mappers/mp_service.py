from src.application.modules.fetchers.fetcher_spec import Spec
from src.interface.api.dtos.dto_service import ProtocolSpecDTO

def protocol_spec_to_dto(spec: Spec) -> ProtocolSpecDTO:
    return ProtocolSpecDTO(
        server_base=spec.server_base,
        endpoint_spec=spec.endpoint_spec,
        full_link=spec.full_link,
        params=spec.params
    )

def dto_to_protocol_spec(dto: ProtocolSpecDTO) -> Spec:
    return Spec(
        server_base=dto.server_base,
        endpoint_spec=dto.endpoint_spec,
        full_link=dto.full_link,
        params=dto.params
    )
