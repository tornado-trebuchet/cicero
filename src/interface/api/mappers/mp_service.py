from src.application.modules.fetchers.fetcher_spec import FetcherSpec
from src.application.modules.text_services.extractor.extractor_spec import (
    ExtractionSpec,
)
from src.domain.models.common.v_common import UUID
from src.interface.api.dtos.dto_service import (
    ExtractionSpecDTO,
    ProtocolSpecDTO,
)


def protocol_spec_to_dto(spec: FetcherSpec) -> ProtocolSpecDTO:
    return ProtocolSpecDTO(
        server_base=spec.server_base,
        endpoint_spec=spec.endpoint_spec,
        full_link=spec.full_link,
        params=spec.params,
    )


def dto_to_protocol_spec(dto: ProtocolSpecDTO) -> FetcherSpec:
    return FetcherSpec(
        server_base=dto.server_base,
        endpoint_spec=dto.endpoint_spec,
        full_link=dto.full_link,
        params=dto.params,
    )


def dto_to_extraction_spec(dto: ExtractionSpecDTO) -> ExtractionSpec:
    return ExtractionSpec(
        protocol=UUID(dto.protocol),
        country=dto.country,
        institution=dto.institution,
        language=dto.language,
        protocol_type=dto.protocol_type,
        pattern_spec=dto.pattern_spec,
    )
