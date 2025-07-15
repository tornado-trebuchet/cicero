from abc import ABC, abstractmethod
from typing import Any
from src.domain.models.text.a_protocol import Protocol
from src.application.modules.fetchers.spec import Spec

class BaseFetcher(ABC):
    """Abstract orchestrator for fetching and storing protocols from external APIs."""

    def __init__(self, api: Any, repository: Any, spec: Spec) -> None:
        self._api = api
        self._repository = repository
        self._spec = spec

    @abstractmethod
    def fetch_single(self) -> Protocol:
        pass

    @abstractmethod
    def fetch_list(self) -> list[Protocol]:
        pass