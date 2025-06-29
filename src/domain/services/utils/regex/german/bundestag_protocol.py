import re 
from src.domain.models.common.v_enums import LanguageEnum, InstitutionTypeEnum, CountryEnum, ExtensionEnum, ProtocolTypeEnum
from src.domain.services.utils.regex.base_regex import BaseRegexPattern

class BundestagProtocolRegex(BaseRegexPattern):

    country_code = CountryEnum.GERMANY
    institution_code = InstitutionTypeEnum.PARLIAMENT
    language_code = LanguageEnum.DE
    protocol_type = ProtocolTypeEnum.PLENARY
    protocol_extension = ExtensionEnum.JSON

    start_pattern = r"\nBeginn: \d{1,2}\.\d{2} Uhr"
    end_pattern = r"\n\(Schluss: \d{1,2}\.\d{2} Uhr\)"

    @staticmethod
    def compile_start_pattern():
        return re.compile(BundestagProtocolRegex.start_pattern)

    @staticmethod
    def compile_end_pattern():
        return re.compile(BundestagProtocolRegex.end_pattern)