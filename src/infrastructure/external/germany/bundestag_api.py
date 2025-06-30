from src.infrastructure.external.base_api import API
from domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from domain.models.text.e_protocol import Protocol
from infrastructure.external.germany.response_mapper import response_to_domain # MAPPER
import requests
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

api_url = "https://search.dip.bundestag.de/api/v1/plenarprotokoll-text"
api_key = "OSOegLs.PR2lwJ1dwCeje9vTj7FPOt3hvpYKtwKkhw"

@dataclass
class Response:
    """
    Parsed response does not represent an internal structure of the actual respons
    """
    date: Optional[str] = None # from response | datum
    title: Optional[str] = None # from response | titel
    link: Optional[str] = None # from response | fundstelle -> pdf_url
    agenda: Optional[Dict[str, Any]] = None # from response | vorgangsbezug -> titel, vorgangstyp
    text: Optional[str] = None # from response | text

class BundestagAPI(API):
    """
    API for fetching data from the German Bundestag.
    """

    @property
    def country(self) -> CountryEnum:
        return CountryEnum.GERMANY

    @property
    def institution(self) -> InstitutionTypeEnum:
        return InstitutionTypeEnum.PARLIAMENT

    @property
    def endpoint_spec(self) -> str:
        return "plenarprotokoll-text"

    def parse_response(self, response: Dict[str, Any]) -> Response:
        """
        Parses the raw response from the Bundestag API into a structured Response object.
        """
        return Response(
            date=response.get('datum'), # specify
            title=response.get('titel'), # specify 
            link=response.get('fundstelle', {}).get('pdf_url'),
            agenda=response.get('vorgangsbezug'), # fix 
            text=response.get('text')
        )


    def fetch_protocol(self, **params) -> Protocol:
        """
        Fetches plenary protocols from the Bundestag API 
        and returns a list of mapped Protocol domain objects.
        """
        request_config = params.get('request_config', None)  # Placeholder for future config

        headers = {"Authorization": f"ApiKey {api_key}"}
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        protocol_dict = self.parse_response(data)
        protocol = response_to_domain(protocol_dict)
        return protocol











