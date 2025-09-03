from typing import Any, Dict
from backend.application.modules.fetchers.base_fetcher import BaseFetcher
from backend.application.modules.fetchers.fetcher_spec import FetcherSpec
from backend.domain.models.text.a_protocol import Protocol
from backend.infrastructure.external.germany.bundestag_api import BundestagAPI
from backend.infrastructure.external.germany.protocol_dto import GermanResponseProtocolDTO
from backend.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
from backend.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from backend.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from backend.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository # To interface
from backend.domain.models.common.v_common import UUID, DateTime, HttpUrl
from backend.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum, ProtocolTypeEnum
from backend.domain.models.text.v_protocol_text import ProtocolText
from backend.domain.models.text.v_protocol_agenda import Agenda
from backend.domain.models.context.v_label import Label
from backend.domain.models.common.v_metadata_plugin import MetadataPlugin
import logging

"""
to async: 
1) Async function 
2) Semaphore 
3) Test event loop 
4) Asynchttp
5) Async DB session * 


"""

logger = logging.getLogger(__name__)

# TODO: Depend on repo contracts + and could simplify this to one single module with DI dependency 
class BundestagFetcher(BaseFetcher):
    """Fetcher for orchestrating Bundestag API protocol acquisition"""

    def __init__(
        self,
        api: BundestagAPI,
        repository: ProtocolRepository,
        spec: FetcherSpec,
    ) -> None:
        super().__init__(api, repository, spec)
        self._limit = self._set_fetch_limit()
        self._joint_q_repo = JointQRepository()
        self._country_repo = CountryRepository()
        self._institution_repo = InstitutionRepository()
        self._country = CountryEnum.GERMANY
        logger.info(f"BundestagFetcher initialized with fetch limit: {self._limit}")

    def fetch_single(self) -> Protocol:
        """Fetch a protocol from the Bundestag API"""
        # Build request and fetch response
        url = self._api.build_request(self._spec.get_spec_dict())
        response = self._api.fetch(url)
        protocol_dto = self._api.parse(response)
        
        # Check for duplicates by source
        source_url = HttpUrl(protocol_dto.source)
        if self._repository.exists(source_url):
            # Return existing protocol instead of creating duplicate
            existing_protocols = self._repository.get_by_source(source_url)
            return existing_protocols[0]
        
        # Convert DTO to domain entity
        protocol = self._from_dto(protocol_dto)
        
        # Persist protocol
        self._repository.add(protocol)
        return protocol

    def fetch_list(self) -> list[UUID]:
        """Fetch multiple protocols from the Bundestag API and store them in the repository."""
        # Get list of protocol IDs
        protocols = self._api.list_protocol_ids()
        protocol_ids: list[UUID] = []
        for protocol_id in protocols:
            try:
                # Create new spec with endpoint_val for each ID
                spec_dict = self._spec.get_spec_dict().copy()
                spec_dict["endpoint_val"] = protocol_id
                
                # Create temporary spec and fetch single protocol
                temp_spec = FetcherSpec(
                    server_base=spec_dict.get("server_base"),
                    endpoint_spec=spec_dict.get("endpoint_spec"),
                    endpoint_val=spec_dict.get("endpoint_val"),
                    full_link=spec_dict.get("full_link"),
                    params=spec_dict.get("params")
                )
                
                # Temporarily update spec and fetch single
                original_spec = self._spec
                self._spec = temp_spec
                protocol = self.fetch_single()
                self._spec = original_spec
                
                # Keep only ID in memory
                protocol_ids.append(protocol.id)
                logger.info(f"Fetched protocol {protocol.id} from Bundestag API")

                # Check limit
                if self._limit is not None and len(protocol_ids) >= self._limit:
                    break
                
            except Exception as e:
                print(f"Failed to fetch protocol {protocol_id}: {e}")
                continue
        
        return protocol_ids
# TODO: abstract to get any country
    def _from_dto(self, dto: GermanResponseProtocolDTO) -> Protocol:
        # Get country (Germany)
        country = self._country_repo.get_by_country_enum(self._country)
        if not country:
            raise ValueError("Germany country not found in database")
        
        # Map institution type from DTO
        institution_type = self._map_institution_type(dto.institution)
        institution = self._institution_repo.get_by_country_id_and_type(
            country.id, institution_type
        )
        if not institution:
            raise ValueError(f"Institution {dto.institution} ({institution_type}) not found in database")
        
        # Map protocol type from DTO
        protocol_type = self._map_protocol_type(dto.type)
        
        # Create value objects
        protocol_text = ProtocolText(dto.text)
        agenda = Agenda(dto.agenda) if dto.agenda else None
        label = Label(dto.label) if dto.label else None
        source_url = HttpUrl(dto.source)
        date = DateTime(dto.date)
        metadata = MetadataPlugin(dto.metadata) if dto.metadata else None
        
        # Create and return Protocol
        return Protocol(
            id=UUID.new(),
            institution_id=institution.id,
            date=date,
            protocol_type=protocol_type,
            protocol_text=protocol_text,
            file_source=source_url,
            label=label,
            agenda=agenda,
            metadata=metadata
        )
# TODO: same
    def _map_institution_type(self, institution_str: str) -> InstitutionTypeEnum:
        if institution_str == "BT":
            return InstitutionTypeEnum.PARLIAMENT
        elif institution_str == "BR":
            return InstitutionTypeEnum.FEDERAL_ASSEMBLY
        else:
            raise ValueError(f"Unknown institution type: {institution_str}")

    def _map_protocol_type(self, type_str: str) -> ProtocolTypeEnum:
        if type_str == "Plenarprotokoll":
            return ProtocolTypeEnum.PLENARY
        else:
            raise ValueError(f"Unknown protocol type: {type_str}")
        

    def _set_fetch_limit(self) -> int | None:
        params: Dict[str, Any] = self._spec.get_spec_dict().get("params") or {}
        limit: Any = params.get("limit")
        if limit is not None:
            return int(limit)
        return None