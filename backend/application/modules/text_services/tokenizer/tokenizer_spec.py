from dataclasses import dataclass

from backend.domain.models.common.v_common import UUID


@dataclass
class TokenizerSpec:
    speech: UUID
