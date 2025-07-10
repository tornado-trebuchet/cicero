from typing import List, Optional
from src.domain.models.common.v_common import UUID
from src.domain.models.base_entity import Entity
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.domain.models.context.v_label import Label

class Institution(Entity):
    """Represents an institution e.g., parliament."""
    def __init__(
        self,
        id: UUID,
        country_id: UUID,
        type: InstitutionTypeEnum,
        label: Label,
        protocols: Optional[List[UUID]] = None,
        periodisation: Optional[List[UUID]] = None,
        metadata: Optional[MetadataPlugin] = None,
    ):
        super().__init__(id)
        self._country_id = country_id
        self._institution_type = type
        self._label = label
        self._protocols = protocols if protocols is not None else []
        self._periodisation = periodisation
        self._metadata = metadata

    @property
    def country_id(self) -> UUID:
        return self._country_id

    @property
    def type(self) -> InstitutionTypeEnum:
        return self._institution_type

    @property
    def label(self) -> Label:
        return self._label
    
    @property
    def protocols(self) -> List[UUID]:
        return self._protocols
    
    @protocols.setter
    def protocols(self, value: List[UUID]):
        self._protocols = value
    
    @property
    def periodisation(self) -> Optional[list[UUID]]:
        return self._periodisation

    @periodisation.setter
    def periodisation(self, value: list[UUID]):
        self._periodisation = value

    @property
    def metadata(self) -> Optional[MetadataPlugin]:
        return self._metadata

    @metadata.setter
    def metadata(self, value: MetadataPlugin):
        self._metadata = value

