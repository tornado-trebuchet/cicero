from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

@dataclass
class FetcherSpec:
    server_base: Optional[str]
    endpoint_spec: Optional[str]
    endpoint_val: Optional[str]
    full_link: Optional[str]
    params: Optional[Dict[str, Union[str, list[str]]]] = None

    def get_spec_dict(self) -> dict[str, Optional[Any]]:
        """Convert the Spec to a dictionary."""
        return {
            "server_base": self.server_base,
            "endpoint_spec": self.endpoint_spec,
            "endpoint_val": self.endpoint_val,
            "full_link": self.full_link,
            "params": self.params,
        }
