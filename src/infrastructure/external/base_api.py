from typing import Optional
from abc import ABC, abstractmethod
from src.domain.models.context.e_institution import Institution
from src.domain.models.text.a_protocol import Protocol
from src.domain.models.common.v_common import HttpUrl
from src.domain.models.context.e_period import Period
from src.infrastructure.external.base_response import Response
from src.domain.models.context.a_country import Country
from src.config import APIConfig

class API(ABC):
    """Base class for external APIs."""

    @abstractmethod
    def __init__(
        self,
        config: APIConfig,
        country: Country,
        institution: Institution
    ) -> None:
        """Initialize the API with shared required parameters."""
        self._country = country
        self._institution = institution

    @property
    @abstractmethod
    def country(self) -> Country:
        """Country for the API."""
        return self._country

    @property
    @abstractmethod
    def institution(self) -> Institution:
        """Institution type for the API."""
        return self._institution

    @property
    @abstractmethod
    def endpoint_spec(self) -> str:
        """Endpoint specification string. URL for fetching a protocol"""
        ...

    @abstractmethod
    def build_request(
        self,
        protocol_spec: str,
        period: Optional[Period] = None,
        params: Optional[dict] = None
    ) -> HttpUrl:
        """Construct the request URL for the API call."""
        ...

    @abstractmethod
    def fetch_protocol(
        self,
        url: HttpUrl
    ) -> Response:
        """Fetch data from the external API using the constructed URL."""
        ...

    @abstractmethod
    def parse_response(self, response: Response) -> Protocol:
        """Parse the API response and convert it to a Protocol domain object."""
        ...