from dataclasses import dataclass

from src.domain.models.common.v_common import UUID


@dataclass
class PreprocessorSpec:
    speech: UUID
