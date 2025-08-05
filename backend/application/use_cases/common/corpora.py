from typing import List, Dict, Any, Callable

from backend.application.use_cases.common.corpora_spec import CorporaSpec
from backend.domain.models.common.a_corpora import Corpora
from backend.domain.models.text.a_speech import Speech
from backend.domain.models.context.e_period import Period
from backend.domain.models.common.v_common import UUID
from backend.domain.models.context.v_label import Label
from backend.domain.models.text.e_text_raw import RawText
from backend.domain.models.text.e_text_clean import CleanText
from backend.domain.models.text.e_text_tokenized import TokenizedText
from backend.domain.models.text.e_text_ngrams import NGramizedText
from backend.domain.irepository.context.i_period import IPeriodRepository
from backend.domain.irepository.common.i_joint_q import IJointQRepository
from backend.domain.irepository.common.i_corpora import ICorporaRepository
from backend.domain.irepository.text.i_text_raw import IRawTextRepository
from backend.domain.irepository.text.i_text_clean import ICleanTextRepository
from backend.domain.irepository.text.i_text_tokenized import ITokenizedTextRepository
from backend.domain.irepository.text.i_text_ngrams import INGramizedTextRepository
from backend.application.di.di_common import get_corpora_spec_repositories

class CorporaManger:
    def __init__(
        self,
        corpora_repo: ICorporaRepository,
        joint_q_repo: IJointQRepository,
        period_repo: IPeriodRepository,
        raw_text_repo: IRawTextRepository,
        clean_text_repo: ICleanTextRepository,
        tokenized_text_repo: ITokenizedTextRepository,
        ngramized_text_repo: INGramizedTextRepository,
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
            periods=periods,
        )

        # Extract UUIDs from speeches
        speech_uuids = {speech.id for speech in speeches}
        # Create descriptive label
        label = self._create_label(corpora_spec)

        corpora = Corpora(
            id=UUID.new(),
            label=label,
            texts=speech_uuids,
            countries=corpora_spec.countries,
            institutions=corpora_spec.institutions,
            protocols=corpora_spec.protocols,
            parties=corpora_spec.parties,
            speakers=corpora_spec.speakers,
            periods=corpora_spec.periods,
        )
        self.corpora_repo.add(corpora)
        return corpora

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

    def get_corpora_by_id(self, corpora_id: UUID) -> Corpora:
        corpora = self.corpora_repo.get_by_id(corpora_id)
        if corpora is None:
            raise ValueError(f"Corpora with id {corpora_id} not found")
        return corpora
    
    # Yeeeeeeeaaahhh, but it works though
    def _create_label(self, corpora_spec: CorporaSpec, repos: Callable[[], Dict[str, Any]] = get_corpora_spec_repositories) -> Label:
        """
        Create a descriptive label from CorporaSpec fields.
        For large collections, shows count and 3 exemplary values.
        """
        repositories: Dict[str, Any] = repos()
        label_parts: List[str] = []
        
        # Countries
        if corpora_spec.countries:
            count = len(corpora_spec.countries)
            if count <= 3:
                # Show all country names
                country_names: List[str] = []
                for country_id in corpora_spec.countries:
                    country = repositories["country"].get_by_id(country_id)
                    if country:
                        country_names.append(country.country.value.title())
                if country_names:
                    label_parts.append(f"{', '.join(country_names)}")
            else:
                # Show count and first 3 examples
                country_names: List[str] = []
                for country_id in corpora_spec.countries[:3]:
                    country = repositories["country"].get_by_id(country_id)
                    if country:
                        country_names.append(country.country.value.title())
                if country_names:
                    label_parts.append(f"{count} Countries: {', '.join(country_names)}...")
        
        # Institutions
        if corpora_spec.institutions:
            count = len(corpora_spec.institutions)
            if count <= 3:
                # Show all institution labels
                institution_names: List[str] = []
                for institution_id in corpora_spec.institutions:
                    institution = repositories["institution"].get_by_id(institution_id)
                    if institution:
                        institution_names.append(institution.label.value)
                if institution_names:
                    label_parts.append(f"{', '.join(institution_names)}")
            else:
                # Show count and first 3 examples
                institution_names: List[str] = []
                for institution_id in corpora_spec.institutions[:3]:
                    institution = repositories["institution"].get_by_id(institution_id)
                    if institution:
                        institution_names.append(institution.label.value)
                if institution_names:
                    label_parts.append(f"{count} Institutions: {', '.join(institution_names)}...")
        
        # Protocols
        if corpora_spec.protocols:
            count = len(corpora_spec.protocols)
            if count <= 3:
                # Show all protocol labels
                protocol_names: List[str] = []
                for protocol_id in corpora_spec.protocols:
                    protocol = repositories["protocol"].get_by_id(protocol_id)
                    if protocol and protocol.label:
                        protocol_names.append(protocol.label.value)
                if protocol_names:
                    label_parts.append(f"{', '.join(protocol_names)}")
                else:
                    label_parts.append(f"{count} Protocols")
            else:
                # Show count and first 3 examples
                protocol_names: List[str] = []
                for protocol_id in corpora_spec.protocols[:3]:
                    protocol = repositories["protocol"].get_by_id(protocol_id)
                    if protocol and protocol.label:
                        protocol_names.append(protocol.label.value)
                if protocol_names:
                    label_parts.append(f"{count} Protocols: {', '.join(protocol_names)}...")
                else:
                    label_parts.append(f"{count} Protocols")
        
        # Parties
        if corpora_spec.parties:
            count = len(corpora_spec.parties)
            if count <= 3:
                # Show all party names
                party_names: List[str] = []
                for party_id in corpora_spec.parties:
                    party = repositories["party"].get_by_id(party_id)
                    if party:
                        party_names.append(party.party_name.value)
                if party_names:
                    label_parts.append(f"{', '.join(party_names)}")
            else:
                # Show count and first 3 examples
                party_names: List[str] = []
                for party_id in corpora_spec.parties[:3]:
                    party = repositories["party"].get_by_id(party_id)
                    if party:
                        party_names.append(party.party_name.value)
                if party_names:
                    label_parts.append(f"{count} Parties: {', '.join(party_names)}...")
        
        # Speakers
        if corpora_spec.speakers:
            count = len(corpora_spec.speakers)
            if count <= 3:
                # Show all speaker names
                speaker_names: List[str] = []
                for speaker_id in corpora_spec.speakers:
                    speaker = repositories["speaker"].get_by_id(speaker_id)
                    if speaker:
                        speaker_names.append(speaker.name.value)
                if speaker_names:
                    label_parts.append(f"{', '.join(speaker_names)}")
            else:
                # Show count and first 3 examples
                speaker_names: List[str] = []
                for speaker_id in corpora_spec.speakers[:3]:
                    speaker = repositories["speaker"].get_by_id(speaker_id)
                    if speaker:
                        speaker_names.append(speaker.name.value)
                if speaker_names:
                    label_parts.append(f"{count} Speakers: {', '.join(speaker_names)}...")
        
        # Periods
        if corpora_spec.periods:
            count = len(corpora_spec.periods)
            if count <= 3:
                # Show all period labels
                period_names: List[str] = []
                for period_id in corpora_spec.periods:
                    period = repositories["period"].get_by_id(period_id)
                    if period:
                        period_names.append(period.label.value)
                if period_names:
                    label_parts.append(f"{', '.join(period_names)}")
            else:
                # Show count and first 3 examples
                period_names: List[str] = []
                for period_id in corpora_spec.periods[:3]:
                    period = repositories["period"].get_by_id(period_id)
                    if period:
                        period_names.append(period.label.value)
                if period_names:
                    label_parts.append(f"{count} Periods: {', '.join(period_names)}...")
        
        # Create final label
        if label_parts:
            label_text = " | ".join(label_parts)
        else:
            label_text = "General Corpora"
        
        return Label(label_text)

