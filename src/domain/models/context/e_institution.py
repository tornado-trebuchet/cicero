from typing import List, Optional
from src.domain.models.common.v_common import UUID
from src.domain.models.base_model import Entity
from domain.models.context.e_period import Period
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.domain.models.common.v_metadata_plugin import MetadataPlugin

class Institution(Entity):
    """Represents an institution e.g., parliament."""
    def __init__(
        self,
        id: UUID,
        country_id: UUID,
        institution_type: InstitutionTypeEnum,
        protocols: Optional[List[UUID]] = None,
        periodisation: Optional[List[Period]] = None,
        metadata: Optional[MetadataPlugin] = None,
    ):
        super().__init__(id)
        self._country_id = country_id
        self._institution_type = institution_type
        self._protocols = protocols if protocols is not None else []
        self._periodisation = periodisation
        self._metadata = metadata

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
    def metadata(self) -> Optional[MetadataPlugin]:
        return self._metadata

    @metadata.setter
    def metadata(self, value: MetadataPlugin):
        self._metadata = value

