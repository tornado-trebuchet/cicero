from typing import Optional, Dict, Any
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository

class CreateInstitutionUseCase:
    def __init__(self):
        self.repository = InstitutionRepository()

    def execute(self, id: UUID, country_id: UUID, type: InstitutionTypeEnum, metadata: Optional[Dict[str, Any]] = None):
        institution = Institution(
            id=id,
            country_id=country_id,
            type=type,
            metadata=MetadataPlugin(metadata) if metadata else None
        )
        self.repository.add(institution)
        return institution
