import pytest
from src.domain.models.common.v_enums import PartyEnumRegistry, CountryEnum, GermanyPartyEnum, FrancePartyEnum
from enum import Enum

# Test correct mapping for Germany
def test_for_country_germany():
    enum_cls = PartyEnumRegistry.for_country(CountryEnum.GERMANY)
    assert enum_cls is GermanyPartyEnum
    assert issubclass(enum_cls, Enum)
    assert enum_cls.CDU.value == "CDU/CSU"

# Test correct mapping for France
def test_for_country_france():
    enum_cls = PartyEnumRegistry.for_country(CountryEnum.FRANCE)
    assert enum_cls is FrancePartyEnum
    assert issubclass(enum_cls, Enum)
    assert enum_cls.LREM.value == "LREM"

# Test ValueError for unsupported country
def test_for_country_unsupported():
    class DummyCountry(str, Enum):
        ITALY = "ITALY"
    with pytest.raises(ValueError) as excinfo:
        PartyEnumRegistry.for_country(DummyCountry.ITALY)  # type: ignore
    assert "No PartyEnum defined for country" in str(excinfo.value)
