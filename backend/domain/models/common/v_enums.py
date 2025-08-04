from enum import Enum


class CountryEnum(str, Enum):
    GERMANY = "Germany"
    FRANCE = "France"


class InstitutionTypeEnum(str, Enum):
    PARLIAMENT = "Parliament"
    FEDERAL_ASSEMBLY = "Feaderal Assembly"


class ProtocolTypeEnum(str, Enum):
    PLENARY = "Plenary"
    HEARING = "Hearing"


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class LanguageEnum(str, Enum):
    DE = "german"
    FR = "french"
    EN = "english"
    M = "missing"


class OwnerTypeEnum(str, Enum):
    COUNTRY = "country"
    INSTITUTION = "institution"
    PARTY = "party"
    SPEAKER = "speaker"



# ------------ Runtime Configuration Enums -------

class PipelineType(Enum):
    """Different types of pipeline execution"""
    FULL = "full"  # Fetch → Extract → Preprocess → Model
    CUSTOM = "custom"  # Custom step selection
    FETCH = "fetch"
    EXTRACT = "extract"
    PREPROCESS = "preprocess"
    TOPIC_MODEL = "topic_model"


class PipelineStep(Enum):
    """Individual pipeline steps"""
    FETCH = "fetch"
    EXTRACT = "extract"  
    PREPROCESS = "preprocess"
    TOPIC_MODEL = "topic_model"
