from src.application.modules.fetchers.base_fetcher import BaseFetcher
from src.application.modules.fetchers.fetcher_spec import FetcherSpec
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.text.a_protocol import Protocol
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.repository.pgsql.common.rep_joint_q import (
    JointQRepository,
)
from src.infrastructure.repository.pgsql.text.rep_protocol import (
    ProtocolRepository,
)


# TODO: Duplicates problem do I need a factory? Or repo method?
class BundestagFetcher(BaseFetcher):
    """Fetcher for orchestrating Bundestag API protocol acquisition and DB storage."""

    def __init__(
        self,
        api: BundestagAPI,
        repository: ProtocolRepository,
        spec: FetcherSpec,
    ) -> None:
        super().__init__(api, repository, spec)
        self._joint_q_repo = JointQRepository()
        self._institution = self._joint_q_repo.get_institution_by_country_and_institution_enum(
            CountryEnum.GERMANY, InstitutionTypeEnum.PARLIAMENT
        )
        self._institution_id = self._institution.id if self._institution else None

    def fetch_single(self) -> Protocol:
        """Fetch a protocol from the Bundestag API and store it in the repository."""
        url = self._api.build_request(self._spec.get_spec_dict())
        response = self._api.fetch(url)
        protocol = self._api.parse(response, self._institution_id)
        self._repository.add(protocol)
        return protocol

    # FIXME: broken
    def fetch_list(self) -> list[Protocol]:
        """Fetch multiple protocols from the Bundestag API and store them in the repository."""
        url = self._api.build_request()
        response = self._api.fetch(url)
        protocols = self._api.parse(response, self._institution_id)
        for protocol in protocols:
            self._repository.add(protocol)
        return protocols
