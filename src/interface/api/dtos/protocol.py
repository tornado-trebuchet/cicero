from pydantic import BaseModel

class ProtocolFetchRequest(BaseModel):
    protocol_id: str

class ProtocolFetchResponse(BaseModel):
    success: bool
    message: str
    protocol_id: str | None = None
