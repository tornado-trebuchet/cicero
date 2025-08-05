from backend.application.use_cases.common.seed_defaults import SeedDefaultsUseCase
# from backend.infrastructure.repository.pgsql.common.rep_corpora import CorporaRepository
# from backend.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
# from backend.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository
# from backend.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
# from backend.infrastructure.repository.pgsql.text.rep_text_tokenized import TokenizedTextRepository
# from backend.infrastructure.repository.pgsql.text.rep_text_ngrams import NGramizedTextRepository
# from backend.application.use_cases.common.corpora import CorporaManger
from backend.infrastructure.repository.pgsql.context.rep_period import PeriodRepository
from backend.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from backend.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from backend.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from backend.infrastructure.repository.pgsql.context.rep_party import PartyRepository
from backend.infrastructure.repository.pgsql.context.rep_speaker import SpeakerRepository

# Suck my balls 
def get_seed_defaults_use_case():
    return SeedDefaultsUseCase()

# FIXME: outdated
# def get_corpora_by_id_use_case():
#     return CorporaManger(
#         corpora_repo=CorporaRepository(),
#         joint_q_repo=JointQRepository(),
#         period_repo=PeriodRepository(),
#         raw_text_repo=RawTextRepository(),
#         clean_text_repo=CleanTextRepository(),
#         tokenized_text_repo=TokenizedTextRepository(),
#         ngramized_text_repo=NGramizedTextRepository(),
#     )

def get_corpora_spec_repositories():
    return {
        "country": CountryRepository(),
        "institution": InstitutionRepository(),
        "protocol": ProtocolRepository(),
        "party": PartyRepository(),
        "speaker": SpeakerRepository(),
        "period": PeriodRepository(),
    }
