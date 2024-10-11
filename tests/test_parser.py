# standard library
from pathlib import Path

# first party
from AstronomicalAnnualCalendar.parser import Parser

# local
from .constants import sample_data_metadata


def test_model_post_init(path_sun_10d: Path):
    parser = Parser(file_path=path_sun_10d)
    assert parser.file == path_sun_10d
    assert parser.metadata == sample_data_metadata
