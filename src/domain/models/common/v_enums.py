from enum import Enum

class CountryEnum(str, Enum):
    GERMANY = "GERMANY"
    FRANCE = "FRANCE"

class InstitutionTypeEnum(str, Enum):
    PARLIAMENT = "PARLIAMENT"
    FEDERAL_ASSEMBLY = "FEDERAL_ASSEMBLY"

class ProtocolTypeEnum(str, Enum):
    PLENARY = "PLENARY"
    HEARING = "HEARING"

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NR = "NR"

class LanguageEnum(str, Enum):
    DE = "german"
    FR = "french"
    EN = "english"
