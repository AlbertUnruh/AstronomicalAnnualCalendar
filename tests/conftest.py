# standard library
from pathlib import Path

# third party
from pytest import fixture


_BASE_PATH: Path = Path(__file__).parent


@fixture
def path_complete_10d() -> Path:
    """Every object; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/complete-10d.txt")


@fixture
def path_mercury_10d() -> Path:
    """Mercury; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/mercury-10d.txt")


@fixture
def path_neptune_1d() -> Path:
    """Neptune; 1-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/neptune-1d.txt")


@fixture
def path_neptune_10d() -> Path:
    """Neptune; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/neptune-10d.txt")


@fixture
def path_sun_10d() -> Path:
    """Sun; 10-day interval; limited calculations;"""
    return _BASE_PATH / Path("sample_data/sun-10d.txt")


@fixture
def path_sun_moon_mercury_10d_everything() -> Path:
    """Sun, moon and mercury; 10-day interval; all calculations;"""
    return _BASE_PATH / Path("sample_data/sun,moon,mercury-10d-everything.txt")
