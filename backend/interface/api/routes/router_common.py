from fastapi import APIRouter, HTTPException, Depends
from backend.application.di.di_common import get_corpora_repository
from backend.interface.api.dtos.dto_common import CorporaSpecDTO, UUIDResponse, CorporaDTO
from backend.interface.api.mappers.mp_common import dto_to_corpora_spec, corpora_to_dto
from backend.application.use_cases.common.corpora import CorporaManger
from backend.domain.models.common.v_common import UUID
from backend.infrastructure.repository.pgsql.common.rep_corpora import CorporaRepository
from backend.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_tokenized import TokenizedTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_ngrams import NGramizedTextRepository
from backend.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
from backend.infrastructure.repository.pgsql.context.rep_period import PeriodRepository

common_router = APIRouter()


@common_router.post("/common/corpora/assemble", response_model=UUIDResponse)
def assemble_corpora(spec_dto: CorporaSpecDTO):
    try:
        spec = dto_to_corpora_spec(spec_dto) 
        corpora_manager = CorporaManger(
            corpora_repo=CorporaRepository(),
            joint_q_repo=JointQRepository(),
            period_repo=PeriodRepository(),
            raw_text_repo=RawTextRepository(),
            clean_text_repo=CleanTextRepository(),
            tokenized_text_repo=TokenizedTextRepository(),
            ngramized_text_repo=NGramizedTextRepository(),
        )
        corpora = corpora_manager.assemble_corpora(spec)
        return UUIDResponse(id=corpora.id.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Corpora assembly failed: {str(e)}")


@common_router.get("/common/corpora/{corpora_id}", response_model=CorporaDTO)
def get_corpora_by_id(corpora_id: str, corpora_manager: CorporaManger = Depends(get_corpora_repository)):
    try:
        corpora = corpora_manager.get_corpora_by_id(UUID(corpora_id))
        return corpora_to_dto(corpora)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get corpora: {str(e)}")


