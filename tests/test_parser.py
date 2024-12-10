# standard library
from typing import TYPE_CHECKING

# third party
import pytest

# first party
from AstronomicalAnnualCalendar.enums import ObservableObjectEnum
from AstronomicalAnnualCalendar.models import DataModel, MetaDataModel, ObservableObjectModel
from AstronomicalAnnualCalendar.parser import Parser

# local
from .constants import (
    sample_data_metadata_w_equinox,
    sample_data_metadata_wo_equinox,
    sample_data_moon,
    sample_data_saturn,
    sample_data_sun,
)


if TYPE_CHECKING:
    # standard library
    from pathlib import Path


@pytest.mark.parametrize(
    ("path_fixture", "metadata"),
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


@pytest.mark.parametrize(
    ("path_fixture", "expected"),
    [
        ("path_sun_d1_2_everything", _sun := {ObservableObjectEnum.SUN: sample_data_sun}),
        ("path_moon_d1_2_everything", _moon := {ObservableObjectEnum.MOON: sample_data_moon}),
        ("path_saturn_d1_2_everything", _saturn := {ObservableObjectEnum.SATURN: sample_data_saturn}),
        ("path_sun_moon_saturn_d1_2_everything", _sun | _moon | _saturn),
    ],
)
def test_parse(path_fixture: str, expected: dict[ObservableObjectModel, DataModel], request: pytest.FixtureRequest):
    path: Path = request.getfixturevalue(path_fixture)
    parser = Parser(file_path=path)
    for v in expected.values():  # find programmer mistakes before it tests the parser
        assert parser.metadata == v.metadata, "Metadata doesn't match with all expected results!"
    assert parser.parse() == expected
