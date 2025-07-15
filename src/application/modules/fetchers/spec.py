from typing import Optional, Any
from src.domain.models.context.e_period import Period

class Spec():
    def __init__(
        self, 
        token: Optional[str], 
        server_base: Optional[str],
        period: Optional[Period], 
        endpoint_spec: Optional[str],
        endpoint_val: Optional[str],
        full_link: Optional[str]
    ) -> None:
        self.token = token if token else None
        self.server_base = server_base if server_base else None
        self.period = period if period else None
        self.endpoint_spec = endpoint_spec if endpoint_spec else None
        self.endpoint_val = endpoint_val if endpoint_val else None
        self.full_link = full_link if full_link else None

    @property
    def token(self) -> Optional[str]:
        return self._token
    
    @token.setter
    def token(self, value: Optional[str]) -> None:
        self._token = value

    @property
    def server_base(self) -> Optional[str]:
        return self._server_base
    
    @server_base.setter
    def server_base(self, value: Optional[str]) -> None:
        self._server_base = value

    @property
    def full_link(self) -> Optional[str]:
        return self._full_link
    
    @full_link.setter
    def full_link(self, value: Optional[str]) -> None:
        self._full_link = value

    @property
    def period(self) -> Optional[Period]:
        return self._period
    
    @period.setter
    def period(self, value: Optional[Period]) -> None:
        self._period = value
    
    @property
    def endpoint_spec(self) -> Optional[str]:
        return self._endpoint_spec
    
    @endpoint_spec.setter
    def endpoint_spec(self, value: Optional[str]) -> None:
        self._endpoint_spec = value

    @property
    def endpoint_val(self) -> Optional[str]:
        return self._endpoint
    
    @endpoint_val.setter
    def endpoint_val(self, value: Optional[str]) -> None:
        self._endpoint = value
    
    def get_spec_dict(self) -> dict[str, Optional[Any]]:
        """Convert the Spec to a dictionary."""
        return {
            "api_key": self.token,
            "server_base": self.server_base,
            "period": self.period.to_range_dict if self.period else None,
            "endpoint_spec": self.endpoint_spec,
            "endpoint_val": self.endpoint_val,
            "full_link": self.full_link
        }