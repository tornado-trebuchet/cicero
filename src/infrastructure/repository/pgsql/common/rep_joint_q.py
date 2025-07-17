from src.domain.irepository.common.i_joint_q import IJointQRepository
from src.domain.models.common.v_enums import InstitutionTypeEnum, CountryEnum
from src.domain.models.context.e_institution import Institution
from src.infrastructure.orm.context.orm_institution import InstitutionORM
from src.infrastructure.orm.context.orm_country import CountryORM
from src.infrastructure.mappers.context.m_institution import InstitutionMapper
from src.infrastructure.orm.orm_session import session_scope
from src.infrastructure.mappers.context.m_country import CountryMapper
from src.domain.models.context.a_country import Country
from src.domain.models.common.v_common import UUID
from src.infrastructure.mappers.text.m_speech import SpeechMapper
from src.infrastructure.mappers.text.m_speech_text import SpeechTextMapper
from src.infrastructure.mappers.text.m_text_raw import RawTextMapper
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.text.e_text_raw import RawText
from typing import Optional

class JointQRepository(IJointQRepository):
    def get_institution_by_country_and_institution_enum(self, country: CountryEnum, institution_enum: InstitutionTypeEnum) -> Optional[Institution]:
        with session_scope() as session:
            # Find the country id by enum
            country_orm = session.query(CountryORM).filter_by(country=country).one_or_none()
            if not country_orm:
                return None
            # Find the institution by country_id and institution_type
            orm_institution = session.query(InstitutionORM).filter_by(
                country_id=country_orm.id,
                institution_type=institution_enum
            ).one_or_none()
            if orm_institution:
                return InstitutionMapper.to_domain(orm_institution)
            return None

    def get_country_by_institution_id(self, institution_id: UUID) -> Optional[Country]:
        with session_scope() as session:
            # Find the institution by id
            orm_institution = session.query(InstitutionORM).filter_by(id=institution_id.value).one_or_none()
            if not orm_institution:
                return None
            # Get the country associated with the institution
            orm_country = session.query(CountryORM).filter_by(id=orm_institution.country_id).one_or_none()
            if orm_country:
                return CountryMapper.to_domain(orm_country)
            return None
        

    def add_speech_speech_text_and_raw_text(
        self, 
        speech: Speech,
        speech_text: SpeechText,
        raw_text: RawText
    ) -> None:
        with session_scope() as session:

            orm_speech = SpeechMapper.to_orm(speech)
            session.add(orm_speech)

            orm_speech_text = SpeechTextMapper.to_orm(speech_text)
            session.add(orm_speech_text)

            orm_raw_text = RawTextMapper.to_orm(raw_text)
            session.add(orm_raw_text)