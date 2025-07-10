from typing import Optional, Any
from src.application.modules.fetchers.base_fetcher import BaseFetcher
from src.domain.models.text.a_protocol import Protocol
from src.domain.models.context.e_period import Period

class BundestagFetcher(BaseFetcher):
    """Fetcher for orchestrating Bundestag API protocol acquisition and DB storage."""

    def fetch_protocol(
        self,
        protocol_spec: str,
        period: Optional[Period] = None,
        params: Optional[dict[str, Any]] = None
    ) -> Protocol:
        """Fetch a protocol from the Bundestag API and store it in the repository."""
        url = self._api.build_request(protocol_spec, period, params)
        response = self._api.fetch_protocol(url)
        protocol = self._api.parse_response(response)
        self._repository.add(protocol)
        return protocol
    

    # later FIXME:what the fuck is this? LOL U stupid? 
    def fetch_protocols(
        self,
        protocol_spec: str,
        period: Optional[Period] = None,
        params: Optional[dict[str, Any]] = None
    ) -> list[Protocol]:
        """Fetch multiple protocols from the Bundestag API and store them in the repository."""
        url = self._api.build_request(protocol_spec, period, params)
        response = self._api.fetch_protocol(url)
        protocols = self._api.parse_response(response)
        for protocol in protocols:
            self._repository.add(protocol)
        return protocols
