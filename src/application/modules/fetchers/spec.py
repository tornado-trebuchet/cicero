from typing import Optional, Any, Dict, Union

#TODO: add better type consistency and validation
class Spec():
    def __init__(
        self, 
        server_base: Optional[str],
        endpoint_spec: Optional[str],
        full_link: Optional[str],
        params: Optional[Dict[str, Union[str, list[str]]]] = None
    ) -> None:
        self.server_base = server_base if server_base else None
        self.endpoint_spec = endpoint_spec if endpoint_spec else None
        self.full_link = full_link if full_link else None
        self.params = params if params else {}

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
    def endpoint_spec(self) -> Optional[str]:
        return self._endpoint_spec
    
    @endpoint_spec.setter
    def endpoint_spec(self, value: Optional[str]) -> None:
        self._endpoint_spec = value

    @property
    def params(self) -> Dict[str, Union[str, list[str]]]:
        return self._params
    
    @params.setter
    def params(self, value: Optional[Dict[str, Union[str, list[str]]]]) -> None:
        self._params = value if value else {}

    def get_spec_dict(self) -> dict[str, Optional[Any]]:
        """Convert the Spec to a dictionary."""
        return {
            "server_base": self.server_base,
            "endpoint_spec": self.endpoint_spec,
            "full_link": self.full_link,
            "params": self.params
        }