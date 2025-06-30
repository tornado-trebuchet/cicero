from domain.models.text.e_protocol import Protocol
from domain.models.text.v_protocol_text import ProtocolText
from domain.models.text.v_agenda import Agenda
from domain.models.common.v_enums import ExtensionEnum, ProtocolTypeEnum
from domain.models.common.v_common import UUID, DateTime, HttpUrl
from infrastructure.external.germany.bundestag_api import Response
import datetime
import uuid



def response_to_domain(item: Response) -> Protocol:
    """
    Maps a Bundestag API response item to a Protocol domain object.
    """
    protocol_id = UUID(item.get("id", str(uuid.uuid4())))
    institution_id = UUID(item.get("institution_id", str(uuid.uuid4())))  # fallback dummy
    extension = ExtensionEnum.PDF if item.get("fundstelle", {}).get("pdf_url") else ExtensionEnum.XML
    protocol_type = ProtocolTypeEnum.PLENARY
    date_str = item.get("datum") or item.get("date")
    date = DateTime(date_str) if date_str else DateTime(datetime.datetime.now().isoformat())
    text = item.get("text") or item.get("textdata") or ""
    protocol_text = ProtocolText(text)
    agenda = Agenda({})  # No agenda parsing for now
    period = item.get("wahlperiode") or item.get("period")
    period = UUID(str(period)) if period else None
    file_source = item.get("fundstelle", {}).get("pdf_url") or item.get("fundstelle", {}).get("xml_url")
    file_source = HttpUrl(file_source) if file_source else None
    metadata = item

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
