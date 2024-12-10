# standard library
from pathlib import Path

# third party
import pytest

# first party
from tests.typehints import GetTextCallable


_BASE_PATH: Path = Path(__file__).parent


@pytest.fixture
def path_complete_10d() -> Path:
    """Every object; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/10d/complete.txt")


@pytest.fixture
def path_mercury_10d() -> Path:
    """Mercury; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/10d/mercury.txt")


@pytest.fixture
def path_neptune_1d() -> Path:
    """Neptune; 1-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/1d/neptune.txt")


@pytest.fixture
def path_neptune_10d() -> Path:
    """Neptune; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/10d/neptune.txt")


@pytest.fixture
def path_sun_10d() -> Path:
    """Sun; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/10d/sun.txt")


@pytest.fixture
def path_sun_moon_mercury_10d_everything() -> Path:
    """Sun, moon and mercury; 10-day interval; all calculations;"""
    return _BASE_PATH / Path("sample_data/10d/sun,moon,mercury-everything.txt")


@pytest.fixture
def path_sun_d1_2_everything() -> Path:
    return _BASE_PATH / Path("sample_data/d1+2/sun-d1+2.txt")


@pytest.fixture
def path_moon_d1_2_everything() -> Path:
    return _BASE_PATH / Path("sample_data/d1+2/moon-d1+2.txt")


@pytest.fixture
def path_saturn_d1_2_everything() -> Path:
    return _BASE_PATH / Path("sample_data/d1+2/saturn-d1+2.txt")


@pytest.fixture
def path_sun_moon_saturn_d1_2_everything() -> Path:
    return _BASE_PATH / Path("sample_data/d1+2/sun,moon,saturn-d1+2.txt")


@pytest.fixture(scope="session")
def get_text() -> GetTextCallable:
    """
    Equivalent to ``get_text()`` (aka. ``_()``) from AstronomicalAnnualCalendar.

    This functions refers to static translations for testing and is independent on translations for the actual project.
    """
    # first party
    import AstronomicalAnnualCalendar.translations as translations

    return translations._Translations(_BASE_PATH / Path("test_locales")).get_text  # type:ignore  # noqa: SLF001
