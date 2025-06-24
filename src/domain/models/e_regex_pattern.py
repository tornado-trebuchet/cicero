from typing import Optional
from src.domain.models.v_common import UUID
from src.domain.models.base_model import Entity

class RegexPattern(Entity):
    """
    Represents a regex pattern for speech extraction and related metadata.
    """
    def __init__(
        self,
        id: UUID,
        country: UUID,
        institution: UUID,
        pattern: str,
        is_active: bool,
        period: Optional[UUID] = None,
        description: Optional[str] = None,
        version: Optional[int] = None,
    ):
        super().__init__(id)
        self._country = country
        self._institution = institution
        self._period = period
        self._pattern = pattern
        self._description = description
        self._version = version
        self._is_active = is_active

    @property
    def country(self) -> UUID:
        return self._country

    @country.setter
    def country(self, value):
        self._country = value

    @property
    def institution(self) -> UUID:
        return self._institution

    @institution.setter
    def institution(self, value):
        self._institution = value

    @property
    def period(self) -> Optional[UUID]:
        return self._period

    @period.setter
    def period(self, value: Optional[UUID]):
        self._period = value

    @property
    def pattern(self) -> str:
        return self._pattern

    @pattern.setter
    def pattern(self, value: str):
        self._pattern = value

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        self._description = value

    @property
    def version(self) -> Optional[int]:
        return self._version

    @version.setter
    def version(self, value: Optional[int]):
        self._version = value

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._is_active = value


    def activate(self):
        self._is_active = True

    def deactivate(self):
        self._is_active = False

    def new_version(self):
        if self._version is None:
            self._version = 1
        else:
            self._version += 1

    def __repr__(self) -> str:
        return f"<RegexPattern v{self._version} active={self._is_active} {self.id}>"
