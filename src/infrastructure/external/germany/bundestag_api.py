from urllib.parse import urlencode
from typing import Any, Optional, Dict, Union, DefaultDict
from collections import defaultdict

from src.infrastructure.external.base_api import API
from src.infrastructure.external.base_response import ResponseProtocol

from src.domain.models.text.a_protocol import Protocol

from src.domain.models.common.v_enums import ProtocolTypeEnum
from src.domain.models.common.v_common import HttpUrl, UUID, DateTime
from src.domain.models.text.v_protocol_text import ProtocolText
from src.domain.models.text.v_protocol_agenda import Agenda
from src.domain.models.common.v_metadata_plugin import MetadataPlugin

from src.config import APIConfig
import requests


class BundestagAPI(API):
    """API for fetching data from the German Bundestag."""

    def __init__(
        self,
        config: APIConfig,
    ) -> None:
        super().__init__(config)
        self._default_server_base = "https://search.dip.bundestag.de/api/v1"
        self._default_endpoint_spec = "plenarprotokoll-text"
        self._default_params = {
            "f.dokumentnummer": "20/6",
            "format": "json",
            "apikey": "OSOegLs.PR2lwJ1dwCeje9vTj7FPOt3hvpYKtwKkhw"
        }
        self._default_endpoint_val = ""
    # Not a secret, public API key
    def build_request(self, spec: dict[str, Optional[Any]]) -> HttpUrl:
        self._full_link = spec.get('full_link') if spec.get('full_link') else None
        if self._full_link is not None:
            return HttpUrl(self._full_link)
        self._server_base = spec.get('server_base') or self._default_server_base
        self._endpoint_spec = spec.get('endpoint_spec') or self._default_endpoint_spec
        params: Dict[str, Union[str, list[str]]] = dict(self._default_params)
        user_params: Dict[str, Union[str, list[str]]] = spec.get('params') or {}
        params.update(user_params)
        url = f"{self._server_base}/{self._endpoint_spec}"
        if params:
            url += f"?{urlencode(params, doseq=True)}"
        return HttpUrl(url)

    def fetch(self,url: HttpUrl) -> ResponseProtocol:
        headers: dict[str, str] = {}
        response = requests.get(str(url), headers=headers)
        response.raise_for_status()
        data = response.json()
        documents = data.get('documents', [])
        if not documents:
            raise ValueError("No documents found in response")
        doc = documents[0]
        date = doc.get('fundstelle', {}).get('datum') or doc.get('datum')
        title = doc.get('titel')
        link = doc.get('fundstelle').get('pdf_url')
        vorgangsbezug = doc.get('vorgangsbezug', [])
        agenda_dict: DefaultDict[str, list[str]] = defaultdict(list)
        for item in vorgangsbezug:
            typ: str = item.get("vorgangstyp", "Unknown")
            titel: str = item.get("titel", "")
            if titel:
                agenda_dict[typ].append(titel)
        agenda: dict[str, list[str]] = dict(agenda_dict)
        text = doc.get('text')
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
        return ResponseProtocol(
            date=str(date),
            title=str(title),
            link=str(link),
            agenda=agenda,
            text=str(text)
        )

    def parse(self, response: ResponseProtocol, institution_id: UUID) -> Protocol:
        protocol_id = UUID.new() # TODO: rredirect to domain responsibility
        protocol_type = ProtocolTypeEnum.PLENARY 
        date = DateTime(response.date)  
        protocol_text = ProtocolText(response.text)
        agenda = Agenda(response.agenda or {})  
        file_source = HttpUrl(response.link)
        metadata = MetadataPlugin()

        return Protocol(
            id=protocol_id,
            institution_id=institution_id,
            protocol_type=protocol_type,
            date=date,
            protocol_text=protocol_text,
            agenda=agenda,
            file_source=file_source,
            metadata= metadata
        )












