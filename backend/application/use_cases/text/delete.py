from backend.domain.irepository.text.i_protocol import IProtocolRepository
from backend.domain.irepository.text.i_speech import ISpeechRepository
from backend.domain.irepository.text.i_speech_text import ISpeechTextRepository
from backend.domain.irepository.text.i_text_clean import ICleanTextRepository
from backend.domain.irepository.text.i_text_ngrams import INGramizedTextRepository
from backend.domain.irepository.text.i_text_raw import IRawTextRepository
from backend.domain.irepository.text.i_text_split import ITextSentencesRepository
from backend.domain.irepository.text.i_text_tokenized import (
    ITokenizedTextRepository,
)
from backend.domain.irepository.text.i_text_translated import (
    ITranslatedTextRepository,
)
from backend.domain.models.common.v_common import UUID


class DeleteProtocolUseCase:
    def __init__(self, repo: IProtocolRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteSpeechUseCase:
    def __init__(self, repo: ISpeechRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteTextCleanUseCase:
    def __init__(self, repo: ICleanTextRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteNGramizedTextUseCase:
    def __init__(self, repo: INGramizedTextRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteTextRawUseCase:
    def __init__(self, repo: IRawTextRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteTextSplitUseCase:
    def __init__(self, repo: ITextSentencesRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteTokenizedTextUseCase:
    def __init__(self, repo: ITokenizedTextRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteTranslatedTextUseCase:
    def __init__(self, repo: ITranslatedTextRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteSpeechTextUseCase:
    def __init__(self, repo: ISpeechTextRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)
