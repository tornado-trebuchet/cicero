from pydantic import BaseModel
from typing import Optional, Dict, Union

class ProtocolSpecDTO(BaseModel):
    server_base: Optional[str] = None
    endpoint_spec: Optional[str] = None
    full_link: Optional[str] = None
    params: Optional[Dict[str, Union[str, list[str]]]] = None
