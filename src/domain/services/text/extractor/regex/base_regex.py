import re
from abc import ABC, abstractmethod
from typing import Type, TypeVar

from src.domain.models.common.v_enums import (
    CountryEnum,
    InstitutionTypeEnum,
    LanguageEnum,
    ProtocolTypeEnum,
)

T = TypeVar("T", bound="RegexPattern")


class RegexPattern(ABC):
    """
    Abstract base class for all regex pattern classes.
    Enforces required metadata and a compile method contract.
    """

    country_code: CountryEnum
    institution_code: InstitutionTypeEnum
    language_code: LanguageEnum
    protocol_type: ProtocolTypeEnum

    @classmethod
    @abstractmethod
    def compile_pattern(cls) -> re.Pattern[str]:
        """
        Should return a compiled regex pattern (re.Pattern).
        """
        pass

    # TODO: add an override for manual pattern picks
    @classmethod
    def find_by_specifications(
        cls: type[T],
        country_code: CountryEnum,
        institution_code: InstitutionTypeEnum,
        language_code: LanguageEnum,
        protocol_type: ProtocolTypeEnum,
    ) -> Type[T] | None:
        """
        Find a subclass matching the given specifications.
        Returns the class if found, else None.
        """
        for subclass in cls.__subclasses__():
            if (
                (getattr(subclass, "country_code", None) == country_code)
                and (
                    getattr(subclass, "institution_code", None)
                    == institution_code
                )
                and (getattr(subclass, "language_code", None) == language_code)
                and (getattr(subclass, "protocol_type", None) == protocol_type)
            ):
                return subclass
        return None
