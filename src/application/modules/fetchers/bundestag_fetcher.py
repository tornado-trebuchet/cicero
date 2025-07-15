from src.application.modules.fetchers.base_fetcher import BaseFetcher
from src.domain.models.text.a_protocol import Protocol
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.application.modules.fetchers.spec import Spec
from src.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from src.domain.models.context.v_label import Label
class BundestagFetcher(BaseFetcher):
    """Fetcher for orchestrating Bundestag API protocol acquisition and DB storage."""

    def __init__(self, api: BundestagAPI, repository: ProtocolRepository, spec: Spec) -> None:
        super().__init__(api, repository, spec)
        # TODO: this one is cursed
        self._inst_repo = InstitutionRepository()
        self._institution= self._inst_repo.get_by_label(Label("Parliament of Germany"))
        self._institution_id = self._institution.id if self._institution else None

    def fetch_single(self) -> Protocol:
        """Fetch a protocol from the Bundestag API and store it in the repository."""
        url = self._api.build_request(self._spec.get_spec_dict)
        response = self._api.fetch_protocol(url)
        protocol = self._api.parse_response(response, self._institution_id)
        self._repository.add(protocol)
        return protocol
    
    # FIXME: broken
    def fetch_list(self) -> list[Protocol]:
        """Fetch multiple protocols from the Bundestag API and store them in the repository."""
        url = self._api.build_request()
        response = self._api.fetch_protocol(url)
        protocols = self._api.parse_response(response)
        for protocol in protocols:
            self._repository.add(protocol)
        return protocols
