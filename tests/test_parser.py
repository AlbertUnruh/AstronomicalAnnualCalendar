# standard library
from typing import TYPE_CHECKING

# third party
import pytest

# first party
from AstronomicalAnnualCalendar.models import MetaDataModel
from AstronomicalAnnualCalendar.parser import Parser

# local
from .constants import sample_data_metadata_w_equinox, sample_data_metadata_wo_equinox


if TYPE_CHECKING:
    # standard library
    from pathlib import Path


@pytest.mark.parametrize(
    "path_fixture, metadata",
    [
        ("path_sun_10d", sample_data_metadata_wo_equinox),
        ("path_sun_moon_mercury_10d_everything", sample_data_metadata_w_equinox),
    ],
)
def test_model_post_init(path_fixture: str, metadata: MetaDataModel, request: pytest.FixtureRequest):
    path: Path = request.getfixturevalue(path_fixture)
    parser = Parser(file_path=path)
    assert parser.file == path
    assert parser.metadata == metadata
