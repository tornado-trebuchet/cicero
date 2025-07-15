from typing import Optional, Any
from abc import ABC, abstractmethod
from src.domain.models.text.a_protocol import Protocol
from src.domain.models.common.v_common import HttpUrl, UUID
from src.infrastructure.external.base_response import ResponseProtocol
from src.config import APIConfig

class API(ABC):
    """
    Base class for external APIs.
    Gets: request spec. From where? 
    Returns: Protocol.
    """

    @abstractmethod
    def __init__(
        self,
        config: APIConfig,
    ) -> None:
        pass

    @abstractmethod
    def build_request(
        self,
        spec: dict[str, Optional[Any]],
    ) -> HttpUrl:
        """Construct the request URL for the API call."""
        ...

    @abstractmethod
    def fetch(
        self,
        url: HttpUrl
    ) -> ResponseProtocol:
        """Fetch data from the external API using the constructed URL."""
        ...

    @abstractmethod
    def parse(self, response: ResponseProtocol, institution_id: UUID) -> Protocol:
        """Parse the API response and convert it to a Protocol domain object."""
        ...
    
