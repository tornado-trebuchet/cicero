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

class GermanyPartyEnum(str, Enum):
    CDU = "CDU/CSU"
    SPD = "SPD"
    FDP = "FDP"
    GRUENE = "Bundnis 90/Die Gruenen"
    LINKE = "die Linke"
    AFD = "AfD"

class FrancePartyEnum(str, Enum):
    LREM = "LREM"
    LR = "LR"
    PS = "PS"
    RN = "RN"
    EELV = "EELV"
    MODEM = "MODEM"

class PartyEnumRegistry:
    _registry = {
        CountryEnum.GERMANY: GermanyPartyEnum,
        CountryEnum.FRANCE: FrancePartyEnum,
    }

    @classmethod
    def for_country(cls, country: CountryEnum) -> type[Enum]:
        try:
            return cls._registry[country]
        except KeyError:
            raise ValueError(f"No PartyEnum defined for country: {country}")
