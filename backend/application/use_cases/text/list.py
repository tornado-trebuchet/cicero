from typing import List

from backend.domain.irepository.text.i_protocol import IProtocolRepository
from backend.domain.models.text.a_protocol import Protocol


class ListProtocolsUseCase:
    def __init__(self, protocol_repository: IProtocolRepository):
        self.protocol_repository = protocol_repository

    def execute(self) -> List[Protocol]:
        return self.protocol_repository.list()
