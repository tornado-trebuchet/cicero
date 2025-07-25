from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse
import requests
import logging

from src.config import APIConfig
from src.domain.models.common.v_common import HttpUrl
from src.infrastructure.external.base_api import API
from src.infrastructure.external.germany.protocol_dto import GermanResponseProtocolDTO

logger = logging.getLogger(__name__)

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
            "format": "json",
            "apikey": "OSOegLs.PR2lwJ1dwCeje9vTj7FPOt3hvpYKtwKkhw",
        }
        self._list_of_protocols_link = "https://search.dip.bundestag.de/api/v1/plenarprotokoll?f.datum.start=2000-01-01&format=json&apikey=OSOegLs.PR2lwJ1dwCeje9vTj7FPOt3hvpYKtwKkhw"
        self._timeout = 10
    # Not a secret, public API key
    def build_request(self, spec: dict[str, Optional[Any]]) -> HttpUrl:
        self._full_link = spec.get("full_link") if spec.get("full_link") else None
        if self._full_link is not None:
            logger.debug(f"Using full_link: {self._full_link}")
            return HttpUrl(self._full_link)
        self._server_base = spec.get("server_base") or self._default_server_base
        self._endpoint_spec = spec.get("endpoint_spec") or self._default_endpoint_spec
        self._endpoint_val = spec.get("endpoint_val")
        params: Dict[str, Union[str, list[str]]] = dict(self._default_params)
        user_params: Dict[str, Union[str, list[str]]] = spec.get("params") or {}
        params.update(user_params)

        url = f"{self._server_base}/{self._endpoint_spec}"
        if self._endpoint_val:
            url += f"/{self._endpoint_val}"
        if params:
            url += f"?{urlencode(params, doseq=True)}"
        logger.info(f"Built Bundestag API request URL: {url}")
        return HttpUrl(url)

    def fetch(self, url: HttpUrl) -> dict[str, Any]:
        headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9"
        }
        logger.info(f"Fetching data from Bundestag API: {url}")
        response = requests.get(str(url), headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Received data: {str(data)[:500]}")
        return data

    def parse(self, response: dict[str, Any]) -> GermanResponseProtocolDTO:
        # Try documents list first (list endpoint)
        documents = response.get("documents", [])
        if documents:
            doc = documents[0]
        else:
            doc = response
            required_keys = ["id", "titel", "herausgeber", "datum", "dokumentart", "wahlperiode", "text"]
            if not all(k in doc for k in required_keys):
                logger.error("No documents found in response and response is not a protocol object")
                raise ValueError("No documents found in response and response is not a protocol object")

        date = doc.get("fundstelle", {}).get("datum") or doc.get("datum")
        title = doc.get("titel")
        source = doc.get("fundstelle", {}).get("pdf_url")
        institution = doc.get("herausgeber")
        legislative_period = doc.get("wahlperiode")
        protocol_type = doc.get("dokumentart")
        label = doc.get("titel")
        vorgangsbezug = doc.get("vorgangsbezug", [])
        agenda_dict: dict[str, list[str]] = {}
        for item in vorgangsbezug:
            typ: str = item.get("vorgangstyp", "Unknown")
            titel: str = item.get("titel", "")
            if titel:
                if typ not in agenda_dict:
                    agenda_dict[typ] = []
                agenda_dict[typ].append(titel)
        agenda: dict[str, list[str]] = agenda_dict
        text = doc.get("text")
        missing = [
            name
            for name, value in [
                ("date", date),
                ("title", title),
                ("source", source),
                ("institution", institution),
                ("legislative_period", legislative_period),
                ("type", protocol_type),
                ("label", label),
                ("agenda", agenda),
                ("text", text),
            ]
            if value is None
        ]
        if missing:
            logger.error(f"Missing required fields in response: {', '.join(missing)}")
            raise ValueError(f"Missing required fields in response: {', '.join(missing)}")
        metadata: dict[str, Any] = {}
        logger.info(f"Parsed protocol: {title} ({date})")
        return GermanResponseProtocolDTO(
            date=str(date),
            title=str(title),
            source=str(source),
            text=str(text),
            institution=str(institution),
            legislative_period=str(legislative_period),
            type=str(protocol_type),
            label=str(label),
            agenda=agenda,
            metadata=metadata,
        )

    def list_protocol_ids(self) -> list[str]:
        """
        Fetches the list of protocol IDs from the Bundestag API, handling cursor pagination.
        Returns:
            List of protocol IDs as strings.
        """

        ids: list[str] = []
        url = self._list_of_protocols_link
        logger.info(f"Fetching protocol IDs from: {url}")
        
        headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9"
        }

        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            documents = data.get("documents", [])
            ids.extend(doc.get("id") for doc in documents if doc.get("id") is not None)
            
            cursor = data.get("cursor")
            logger.debug(f"Fetched {len(documents)} documents, cursor: {cursor}")
            
            # Break if no cursor OR no documents were returned
            if not cursor or len(documents) == 0:
                break

            # Parse URL and update cursor param SAFELY
            parsed = urlparse(url)
            query_list = parse_qsl(parsed.query, keep_blank_values=True)
            
            # Remove existing cursor and add new raw cursor
            new_query: list[tuple[str, str]] = []
            for key, value in query_list:
                if key == "cursor":
                    continue  # Remove old cursor
                new_query.append((key, value))
            new_query.append(("cursor", cursor))  # Add raw cursor value
            
            # Rebuild URL with original encoding preserved
            url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                urlencode(new_query, doseq=True),
                parsed.fragment
            ))
            logger.debug(f"Next URL: {url}")

        logger.info(f"Total protocol IDs fetched: {len(ids)}")
        return ids
