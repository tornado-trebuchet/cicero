from abc import ABC, abstractmethod
from typing import Optional, Any
from src.domain.models.text.a_protocol import Protocol
from src.domain.models.context.e_period import Period

# TODO: complete redesign!!!!!!! Implement as use case! 
class BaseFetcher(ABC):
    """Abstract orchestrator for fetching and storing protocols from external APIs."""

    def __init__(self, api: Any, repository: Any) -> None:
        """Initialize with an API client and a protocol repository."""
        self._api = api
        self._repository = repository
        # TODO: discover protocol spec based on the called class
    @abstractmethod
    def fetch_protocol(
        self,
        protocol_spec: str,
        period: Optional[Period] = None,
        params: Optional[dict[str, Any]] = None
    ) -> Protocol:
        """Fetch a protocol from the API and store it in the repository."""
        pass

    @abstractmethod
    def fetch_protocols(
        self,
        protocol_spec: str,
        period: Optional[Period] = None,
        params: Optional[dict[str, Any]] = None
    ) -> list[Protocol]:
        """Fetch multiple protocols from the API and store them in the repository."""
        pass