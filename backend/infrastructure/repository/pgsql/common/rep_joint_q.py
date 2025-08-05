from typing import Optional, List

from backend.domain.irepository.common.i_joint_q import IJointQRepository
from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from backend.domain.models.context.a_country import Country
from backend.domain.models.context.e_institution import Institution
from backend.domain.models.context.e_period import Period
from backend.domain.models.text.a_speech import Speech
from backend.domain.models.text.a_speech_text import SpeechText
from backend.domain.models.text.e_text_raw import RawText
from backend.domain.models.text.a_protocol import Protocol
from backend.infrastructure.mappers.context.m_country import CountryMapper
from backend.infrastructure.mappers.context.m_institution import InstitutionMapper
from backend.infrastructure.mappers.text.m_speech import SpeechMapper
from backend.infrastructure.mappers.text.m_speech_text import SpeechTextMapper
from backend.infrastructure.mappers.text.m_text_raw import RawTextMapper
from backend.infrastructure.mappers.text.m_protocol import ProtocolMapper
from backend.infrastructure.orm.context.orm_country import CountryORM
from backend.infrastructure.orm.context.orm_institution import InstitutionORM
from backend.infrastructure.orm.context.orm_speaker import SpeakerORM
from backend.infrastructure.orm.text.orm_speech_text import SpeechTextORM
from backend.infrastructure.orm.text.orm_speech import SpeechORM
from backend.infrastructure.orm.text.orm_protocol import ProtocolORM

from backend.infrastructure.orm.orm_session import session_scope

class JointQRepository(IJointQRepository):
    def get_institution_by_country_and_institution_enum(
        self, country: CountryEnum, institution_enum: InstitutionTypeEnum
    ) -> Optional[Institution]:
        with session_scope() as session:
            # Find the country id by enum
            country_orm = session.query(CountryORM).filter_by(country=country).one_or_none()
            if not country_orm:
                return None
            # Find the institution by country_id and institution_type
            orm_institution = (
                session.query(InstitutionORM)
                .filter_by(
                    country_id=country_orm.id,
                    institution_type=institution_enum,
                )
                .one_or_none()
            )
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

    def get_protocol_by_speech_id(self, speech_id: UUID) -> Optional[Protocol]:
        with session_scope() as session:
            # Find the speech by id
            orm_speech = session.query(SpeechORM).filter_by(id=speech_id.value).one_or_none()
            if not orm_speech:
                return None
            # Get the protocol associated with the speech
            orm_protocol = session.query(ProtocolORM).filter_by(id=orm_speech.protocol_id).one_or_none()
            if orm_protocol:
                return ProtocolMapper.to_domain(orm_protocol)
            return None

    def get_speech_text_by_speech_id(self, speech_id: UUID) -> Optional[SpeechText]:
        with session_scope() as session:
            # Find the speech by id
            orm_speech = session.query(SpeechORM).filter_by(id=speech_id.value).one_or_none()
            if not orm_speech:
                return None
            # Get the speech text associated with the speech
            orm_speech_text = session.query(SpeechTextORM).filter_by(speech_id=orm_speech.id).one_or_none()
            if orm_speech_text:
                return SpeechTextMapper.to_domain(orm_speech_text)
            return None

    def add_speech_speech_text_and_raw_text(
        self, speech: Speech, speech_text: SpeechText, raw_text: RawText
    ) -> None:
        with session_scope() as session:

            orm_speech = SpeechMapper.to_orm(speech)
            session.add(orm_speech)

            orm_speech_text = SpeechTextMapper.to_orm(speech_text)
            session.add(orm_speech_text)

            orm_raw_text = RawTextMapper.to_orm(raw_text)
            session.add(orm_raw_text)


# FIXME: THIS SHIT IS BROKEN
    def get_speeches_with_filter(
        self,
        countries: Optional[List[UUID]] = None,
        institutions: Optional[List[UUID]] = None,
        protocols: Optional[List[UUID]] = None,
        party_ids: Optional[List[UUID]] = None,
        speaker_ids: Optional[List[UUID]] = None,
        periods: Optional[List[Period]] = None,
    ) -> list[Speech]:
        """
        Get speeches with optional filters.
        All provided filters are combined with AND operations.
        If a filter is None, it is not applied.
        """
        with session_scope() as session:
            # Start with a basic query for speeches
            query = session.query(SpeechORM)

            # Keep track of joins to avoid duplicate joins
            joined_protocol = False
            joined_institution = False
            joined_speaker = False

            # Apply country filter if provided
            if countries and len(countries) > 0:
                country_values = [country.value for country in countries]
                # We need to join through protocol to institution to country
                if not joined_protocol:
                    query = query.join(SpeechORM.protocol)
                    joined_protocol = True

                if not joined_institution:
                    query = query.join(ProtocolORM.institution)
                    joined_institution = True

                query = query.filter(InstitutionORM.country_id.in_(country_values))

            # Apply institution filter if provided
            if institutions and len(institutions) > 0:
                institution_values = [institution.value for institution in institutions]
                if not joined_protocol:
                    query = query.join(SpeechORM.protocol)
                    joined_protocol = True

                query = query.filter(ProtocolORM.institution_id.in_(institution_values))

            # Apply protocol filter if provided
            if protocols and len(protocols) > 0:
                protocol_values = [protocol.value for protocol in protocols]
                query = query.filter(SpeechORM.protocol_id.in_(protocol_values))

            # Apply party filter if provided
            if party_ids and len(party_ids) > 0:
                party_values = [party_id.value for party_id in party_ids]
                if not joined_speaker:
                    query = query.join(SpeechORM.speaker)
                    joined_speaker = True

                query = query.filter(SpeakerORM.party_id.in_(party_values))

            # Apply speaker filter if provided
            if speaker_ids and len(speaker_ids) > 0:
                speaker_values = [speaker_id.value for speaker_id in speaker_ids]
                query = query.filter(SpeechORM.speaker_id.in_(speaker_values))

            # Apply periods filter if provided
            if periods and len(periods) > 0:
                if not joined_protocol:
                    query = query.join(SpeechORM.protocol)
                    joined_protocol = True

                # Handle each period separately
                for period in periods:
                    # For each period, filter by its date range
                    start_date = period.start_date.value
                    end_date = period.end_date.value
                    query = query.filter(ProtocolORM.date >= start_date, ProtocolORM.date <= end_date)


            print(f"Executing query: {query}")
            # Execute the query
            orm_speeches = query.all()
            print(f"Found {len(orm_speeches)} speeches")
            # Map the results to domain objects
            return [SpeechMapper.to_domain(orm_speech) for orm_speech in orm_speeches]
