from typing import List

from src.domain.models.common.a_corpora import Corpora
from src.domain.models.text.a_speech import Speech
from src.domain.irepository.common.i_corpora import ICorporaRepository
from src.application.use_cases.common.corpora_spec import CorporaSpec
from src.domain.irepository.common.i_joint_q import IJointQRepository
from src.domain.irepository.context.i_period import IPeriodRepository
from src.domain.models.context.e_period import Period
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label
from src.domain.models.text.e_text_raw import RawText
from src.domain.models.text.e_text_clean import CleanText
from src.domain.models.text.e_text_tokenized import TokenizedText
from src.domain.models.text.e_text_ngrams import NGramizedText
from src.domain.irepository.text.i_text_raw import IRawTextRepository
from src.domain.irepository.text.i_text_clean import ICleanTextRepository
from src.domain.irepository.text.i_text_tokenized import ITokenizedTextRepository
from src.domain.irepository.text.i_text_ngrams import INGramizedTextRepository

# TODO: Somewhat redundant, since repositories will still have by IDs method 
class CorporaManger: 

    def __init__(
        self, 
        corpora_repo: ICorporaRepository, 
        joint_q_repo: IJointQRepository,
        period_repo: IPeriodRepository,
        raw_text_repo: IRawTextRepository,
        clean_text_repo: ICleanTextRepository,
        tokenized_text_repo: ITokenizedTextRepository,
        ngramized_text_repo: INGramizedTextRepository
    ):
        self.corpora_repo = corpora_repo
        self.joint_q_repo = joint_q_repo
        self.period_repo = period_repo
        self.raw_text_repo = raw_text_repo
        self.clean_text_repo = clean_text_repo
        self.tokenized_text_repo = tokenized_text_repo
        self.ngramized_text_repo = ngramized_text_repo

    def assemble_corpora(self, corpora_spec: CorporaSpec) -> Corpora:
        periods: List[Period] = []
        if corpora_spec.periods:
            for period_id in corpora_spec.periods:
                period_obj = self.period_repo.get_by_id(period_id)
                if period_obj is not None:
                    periods.append(period_obj)
            
        speeches: List[Speech] = self.joint_q_repo.get_speeches_with_filter(
            countries=corpora_spec.countries,
            institutions=corpora_spec.institutions,
            protocols=corpora_spec.protocols,
            party_ids=corpora_spec.parties,
            speaker_ids=corpora_spec.speakers,
            periods=periods
        )
        
        # Extract UUIDs from speeches
        speech_uuids = {speech.id for speech in speeches}
        # TODO: Create label 

        return Corpora(
            id=UUID.new(),
            label=Label("TODO: Replace this thing"),
            texts=speech_uuids,
            countries=corpora_spec.countries,
            institutions=corpora_spec.institutions,
            protocols=corpora_spec.protocols,
            parties=corpora_spec.parties,
            speakers=corpora_spec.speakers,
            periods=corpora_spec.periods
    )

    def get_raw_texts_from_corpora(self, corpora: Corpora) -> List[RawText]:
        return [
            raw_text
            for speech_id in corpora.texts
            if (raw_text := self.raw_text_repo.get_by_speech_id(speech_id)) is not None
        ]

    def get_clean_texts_from_corpora(self, corpora: Corpora) -> List[CleanText]:
        return [
            clean_text
            for speech_id in corpora.texts
            if (clean_text := self.clean_text_repo.get_by_speech_id(speech_id)) is not None
        ]

    def get_tokenized_texts_from_corpora(self, corpora: Corpora) -> List[TokenizedText]:
        return [
            tokenized_text
            for speech_id in corpora.texts
            if (tokenized_text := self.tokenized_text_repo.get_by_speech_id(speech_id)) is not None
        ]

    def get_ngrammed_texts_from_corpora(self, corpora: Corpora) -> List[NGramizedText]:
        return [
            ngrammed_text
            for speech_id in corpora.texts
            if (ngrammed_text := self.ngramized_text_repo.get_by_speech_id(speech_id)) is not None
        ]