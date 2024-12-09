# standard library
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

# third party
import pytest

# first party
from AstronomicalAnnualCalendar.enums import ObservableObjectEnum
from AstronomicalAnnualCalendar.models import DataModel, MetaDataModel, ObservableObjectModel, RowModel
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


_saturn = {
    ObservableObjectEnum.SATURN: DataModel(
        bound_object=ObservableObjectEnum.SATURN,
        metadata=sample_data_metadata_w_equinox,
        rows=[
            RowModel(
                bound_object=ObservableObjectEnum.SATURN,
                date_and_time=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=1))),
                right_ascension="22h21m50.2s",
                declination="-11°57'39\"",
                ecliptic_longitude="332°54'29\"",
                ecliptic_latitude="- 1°37'58\"",
                rise="11h21m",
                culmination="16h16m",
                set="12h10m",
                azimut_rise="110°",
                azimut_set="250°",
            ),
        ],
    )
}


@pytest.mark.parametrize(
    "path_fixture, expected",
    [
        ("path_sun_d1_2_everything", _sun := {}),
        (
            "path_saturn_d1_2_everything",
            _saturn,
        ),
        ("path_sun_saturn_d1_2_everything", _sun | _saturn),
    ],
)
def test_parse(path_fixture: str, expected: dict[ObservableObjectModel, DataModel], request: pytest.FixtureRequest):
    path: Path = request.getfixturevalue(path_fixture)
    parser = Parser(file_path=path)
    assert parser.parse() == expected
