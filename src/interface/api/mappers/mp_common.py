from src.domain.models.common.a_corpora import Corpora
from src.interface.api.dtos.dto_common import CorporaDTO
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label
from src.interface.api.dtos.dto_common import CorporaSpecDTO
from src.application.use_cases.common.corpora_spec import CorporaSpec


def corpora_to_dto(corpora: Corpora) -> CorporaDTO:
    return CorporaDTO(
        id=corpora.id.value,
        label=corpora.label.value,
        texts=[uuid.value for uuid in corpora.texts],
        countries=[uuid.value for uuid in corpora.countries] if corpora.countries else None,
        institutions=[uuid.value for uuid in corpora.institutions] if corpora.institutions else None,
        periods=[uuid.value for uuid in corpora.periods] if corpora.periods else None,
        parties=[uuid.value for uuid in corpora.parties] if corpora.parties else None,
        speakers=[uuid.value for uuid in corpora.speakers] if corpora.speakers else None,
    )

def dto_to_corpora(dto: CorporaDTO) -> Corpora:
    return Corpora(
        id=UUID(dto.id),
        label=Label(dto.label),
        texts={UUID(text_id) for text_id in dto.texts},
        countries=[UUID(country_id) for country_id in dto.countries] if dto.countries else None,
        institutions=[UUID(inst_id) for inst_id in dto.institutions] if dto.institutions else None,
        periods=[UUID(period_id) for period_id in dto.periods] if dto.periods else None,
        parties=[UUID(party_id) for party_id in dto.parties] if dto.parties else None,
        speakers=[UUID(speaker_id) for speaker_id in dto.speakers] if dto.speakers else None,
    )

def dto_to_corpora_spec(dto: CorporaSpecDTO) -> CorporaSpec:
    return CorporaSpec(
        countries=[UUID(country_id) for country_id in dto.countries] if dto.countries else None,
        institutions=[UUID(inst_id) for inst_id in dto.institutions] if dto.institutions else None,
        protocols=[UUID(proto_id) for proto_id in dto.protocols] if dto.protocols else None,
        parties=[UUID(party_id) for party_id in dto.parties] if dto.parties else None,
        speakers=[UUID(speaker_id) for speaker_id in dto.speakers] if dto.speakers else None,
        periods=[UUID(period_id) for period_id in dto.periods] if dto.periods else None,
    )

def corpora_spec_to_dto(spec: CorporaSpec) -> CorporaSpecDTO:
    return CorporaSpecDTO(
        countries=[uuid.value for uuid in spec.countries] if spec.countries else None,
        institutions=[uuid.value for uuid in spec.institutions] if spec.institutions else None,
        protocols=[uuid.value for uuid in spec.protocols] if spec.protocols else None,
        parties=[uuid.value for uuid in spec.parties] if spec.parties else None,
        speakers=[uuid.value for uuid in spec.speakers] if spec.speakers else None,
        periods=[uuid.value for uuid in spec.periods] if spec.periods else None,
    )