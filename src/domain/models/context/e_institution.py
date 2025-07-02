from typing import List, Optional
from src.domain.models.common.v_common import UUID
from src.domain.models.common.base_model import Entity
from src.domain.models.context.v_period import Period
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.domain.models.common.v_metadata_plugin import MetadataPlugin

class Institution(Entity):
    """Represents an institution e.g., parliament."""
    def __init__(
        self,
        id: UUID,
        country_id: UUID,
        institution_type: InstitutionTypeEnum,
        periodisation: List[Period],
        metadata: MetadataPlugin,
    ):
        super().__init__(id)
        self._country_id = country_id
        self._institution_type = institution_type
        self._periodisation = periodisation if periodisation is not None else []
        self._metadata = metadata if metadata is not None else MetadataPlugin({})

    @property
    def country_id(self) -> UUID:
        return self._country_id

    @property
    def institution_type(self) -> InstitutionTypeEnum:
        return self._institution_type

    @property
    def periodisation(self) -> Optional[list[Period]]:
        return self._periodisation

    @periodisation.setter
    def periodisation(self, value: list[Period]):
        self._periodisation = value

    @property
    def metadata(self) -> MetadataPlugin:
        return self._metadata

    @metadata.setter
    def metadata(self, value: MetadataPlugin):
        self._metadata = value

