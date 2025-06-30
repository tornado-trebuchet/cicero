from src.infrastructure.external.base_api import API
from src.infrastructure.external.base_response import Response
from src.domain.models.common.v_enums import CountryEnum, ExtensionEnum, ProtocolTypeEnum
from src.domain.models.common.v_common import HttpUrl, UUID, DateTime
from src.domain.models.text.e_protocol import Protocol
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.ve_period import Period
from src.domain.models.text.v_protocol_text import ProtocolText
from src.domain.models.text.v_agenda import Agenda
from src.config import APIConfig
from typing import Any, Optional, cast
from urllib.parse import urlencode
import requests

class BundestagAPI(API):
    """API for fetching data from the German Bundestag."""

    def __init__(
        self,
        config: APIConfig,
        country: CountryEnum,
        institution: Institution
    ) -> None:
        super().__init__(config, country, institution)
        self._base_url = getattr(config, 'BASE_URL', None)
        self._api_key = getattr(config, 'API_KEY', None)
        self._country = country
        self._institution = institution

    @property
    def country(self) -> CountryEnum:
        return self._country

    @property
    def institution(self) -> Institution:
        return self._institution

    @property
    def endpoint_spec(self) -> str:
        return "plenarprotokoll-text"

    def build_request(
        self,
        protocol_spec: str,
        period: Optional[Period] = None,
        params: Optional[dict] = None
    ) -> HttpUrl:
        """Construct the request URL for the Bundestag plenarprotokoll-text endpoint."""
        base_url = f"{self._base_url}/{self.endpoint_spec}"
        query = {}
        if protocol_spec:
            query["f.dokumentnummer"] = protocol_spec
        if period is not None:
            query["f.wahlperiode"] = str(period)
        if params:
            query.update(params)
        url = base_url
        if query:
            url += "?" + urlencode(query, doseq=True)
        return HttpUrl(url)

    def fetch_protocol(
        self,
        url: HttpUrl
    ) -> Response:
        headers = {"Authorization": f"ApiKey {self._api_key}"} if self._api_key else {}
        response = requests.get(str(url), headers=headers)
        response.raise_for_status()
        data = response.json()
        date = data.get('datum')
        title = data.get('titel')
        link = data.get('fundstelle', {}).get('pdf_url')
        agenda = data.get('vorgangsbezug')
        text = data.get('text')
        missing = [
            name for name, value in [
                ("date", date),
                ("title", title),
                ("link", link),
                ("agenda", agenda),
                ("text", text)
            ] if value is None
        ]
        if missing:
            raise ValueError(f"Missing required fields in response: {', '.join(missing)}")
        return Response(
            date=str(date),
            title=str(title),
            link=str(link),
            agenda=cast(dict[str, Any], agenda),
            text=str(text)
        )

    def parse_response(self, response: Response) -> Protocol:
        protocol_id = UUID.new()
        institution_id = self.institution.id
        extension = ExtensionEnum.PDF  
        protocol_type = ProtocolTypeEnum.PLENARY 
        date = DateTime(response.date)  
        protocol_text = ProtocolText(response.text)
        agenda = Agenda(response.agenda or {})  
        period: Optional[Period] = None
        file_source = HttpUrl(response.link) if response.link else None
        metadata = {}  

        return Protocol(
            id=protocol_id,
            institution_id=institution_id,
            extension=extension,
            protocol_type=protocol_type,
            date=date,
            protocol_text=protocol_text,
            agenda=agenda,
            period=period,
            file_source=file_source,
            metadata=metadata
        )












