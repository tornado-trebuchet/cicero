from src.application.modules.fetchers.base_fetcher import BaseFetcher
from src.application.modules.fetchers.fetcher_spec import FetcherSpec
from src.domain.models.text.a_protocol import Protocol
from src.infrastructure.external.germany.bundestag_api import BundestagAPI
from src.infrastructure.external.germany.protocol_dto import GermanResponseProtocolDTO
from src.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
from src.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from src.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.domain.models.common.v_common import UUID, DateTime, HttpUrl
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum, ProtocolTypeEnum
from src.domain.models.text.v_protocol_text import ProtocolText
from src.domain.models.text.v_protocol_agenda import Agenda
from src.domain.models.context.v_label import Label
from src.domain.models.common.v_metadata_plugin import MetadataPlugin

class BundestagFetcher(BaseFetcher):
    """Fetcher for orchestrating Bundestag API protocol acquisition"""

    def __init__(
        self,
        api: BundestagAPI,
        repository: ProtocolRepository,
        spec: FetcherSpec,
    ) -> None:
        super().__init__(api, repository, spec)
        self._joint_q_repo = JointQRepository()
        self._country_repo = CountryRepository()
        self._institution_repo = InstitutionRepository()
        self._country = CountryEnum.GERMANY

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
                
            except Exception as e:
                print(f"Failed to fetch protocol {protocol_id}: {e}")
                continue
        
        return protocol_ids

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
