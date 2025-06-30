import re
from src.domain.models.common.v_enums import LanguageEnum, InstitutionTypeEnum, CountryEnum, ExtensionEnum, ProtocolTypeEnum
from src.domain.services.utils.regex.base_regex import RegexPattern

class BundestagGeneralRegex(RegexPattern):
    country_code = CountryEnum.GERMANY
    institution_code = InstitutionTypeEnum.PARLIAMENT
    language_code = LanguageEnum.DE
    protocol_type = ProtocolTypeEnum.PLENARY
    protocol_extension = ExtensionEnum.JSON

    speaker_pattern = r"""
    (?mx)
    (?:^|(?:\n\s*){1,5})                                                                     # Must start at beginning of line, multiple newlines
    (?:(?:Präsident(?:in)?|Alterspräsident(?:in)?|Vizepräsident(?:in)?)[\s\xa0,]+)?        # Optional procedural title
    (?:(?:Dr\.|Prof\.|[A-Z][a-z]*\.)\s?(?:[A-Za-z]*\.\s?){0,2})*                           # Optional academic title(s)
(                                                                                     # Group 1: Full name (mandatory first name and surname)
    (?! (?:Kolleg(?:e(?:n)?|in)?|Herr|Frau|Abgeordnet(?:e(?:n)?)?|Antwort|Frage|Der|Die|Das|Liebe(?:r)?)\b ) # Filter out common introducing lines
    [A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ][a-zäöüßçğışéèêëàâîïôùûüÿñæœ]+                       # First name, starting with a capital letter
    (?:[-\s\xa0](?:
        [A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ][a-zäöüßçğışéèêëàâîïôùûüÿñæœ]+|                   # Additional parts of first name (e.g., hyphenated)
        [A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ]\.                                                # OR just an initial with a period
    ))*
    (?:[\s\xa0]+                                                                       # At least one whitespace is required before surname
        (?:                                                                           # Either a direct surname...
            [A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ][a-zäöüßçğışéèêëàâîïôùûüÿñæœ]+               # Surname starting with a capital letter
        |                                                                             # ...or a preposition and then the surname (e.g., "von Korte")
            (?:von|van|de|der|zu|di|del|da|dos|das|de\sla|von\sund\szu)[\s\xa0]+[A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ][a-zäöüßçğışéèêëàâîïôùûüÿñæœ]+
        )
        (?:[-\s\xa0][A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ][a-zäöüßçğışéèêëàâîïôùûüÿñæœ]+)*      # Optional additional parts of surname (e.g., hyphenated)
    )
)
    (?:[\s\xa0]*\(\s*([^)]+?)[\s\xa0]*\))?                                                  # Group 2: Optional first bracket (e.g., Land)
    (?:[\s\xa0]*\(\s*([^)]+?)[\s\xa0]*\))?                                                  # Group 3: Optional second bracket (e.g., Party)
    (?:,\s+                                                                               # Mandatory comma if role info is present                                                                                       
            ([A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ][^\s:]+(?:\s+[^\s:]+){0,9}))?                      # Group 4: Role info (up to 7 words)
    [\s\xa0]*:[\s\xa0]*                                                                   # Mandatory colon delimiter, with optional trailing whitespace/newlines
    (?=[\s\xa0]*\n)[\s\xa0]*\n[\s\xa0]*([A-ZÄÖÜÇĞIŞÉÈÊËÀÂÎÏÔÙÛÜŸÑÆŒ])                                                # Catching the first capital letter
"""

    @classmethod
    def compile_pattern(cls) -> re.Pattern[str]:
        return re.compile(cls.speaker_pattern, re.VERBOSE)



