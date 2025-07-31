from abc import ABC, abstractmethod
from typing import Any

from backend.application.modules.fetchers.fetcher_spec import FetcherSpec
from backend.domain.models.text.a_protocol import Protocol
from backend.domain.models.common.v_common import UUID

class BaseFetcher(ABC):
    """Abstraction for fetching and storing protocols from external APIs."""

    def __init__(self, api: Any, repository: Any, spec: FetcherSpec) -> None:
        self._api = api
        self._repository = repository
        self._spec = spec

    @abstractmethod
    def fetch_single(self) -> Protocol:
        pass

    @abstractmethod
    def fetch_list(self) -> list[UUID]:
        pass
