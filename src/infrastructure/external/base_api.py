from abc import ABC, abstractmethod
from typing import Any
from domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from domain.models.text.e_protocol import Protocol

class API(ABC):
    """
    Base class for external APIs.
    Enforces contract for country, institution, and endpoint specification.
    """
    @property
    @abstractmethod
    def country(self) -> CountryEnum:
        """
        The country for the API (as a CountryEnum).
        This value should be constant for each API implementation.
        """
        ...

    @property
    @abstractmethod
    def institution(self) -> InstitutionTypeEnum:
        """
        The institution that determines the concrete URL (as an InstitutionTypeEnum).
        This value should be constant for each API implementation.
        """
        ...

    @property
    @abstractmethod
    def endpoint_spec(self) -> str:
        """
        The endpoint specification (e.g., period).
        This value should be constant for each API implementation.
        """
        ...

    @abstractmethod
    def fetch_protocol(self, *args, **kwargs) -> Protocol:
        """
        Fetch data from the external API.
        Should return domain model objects (e.g., Protocol).
        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")