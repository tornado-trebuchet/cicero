from src.application.use_cases.common.seed_defaults import SeedDefaultsUseCase
from src.infrastructure.repository.pgsql.common.rep_corpora import CorporaRepository
from src.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
from src.infrastructure.repository.pgsql.context.rep_period import PeriodRepository
from src.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_tokenized import TokenizedTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_ngrams import NGramizedTextRepository
from src.application.use_cases.common.corpora import CorporaManger


def get_seed_defaults_use_case():
    return SeedDefaultsUseCase()


def get_corpora_by_id_use_case():
    return CorporaManger(
        corpora_repo=CorporaRepository(),
        joint_q_repo=JointQRepository(),
        period_repo=PeriodRepository(),
        raw_text_repo=RawTextRepository(),
        clean_text_repo=CleanTextRepository(),
        tokenized_text_repo=TokenizedTextRepository(),
        ngramized_text_repo=NGramizedTextRepository(),
    )
