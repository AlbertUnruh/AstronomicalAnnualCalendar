# standard library
import re
from datetime import timedelta

# third party
import pytest

# first party
from AstronomicalAnnualCalendar.regex import (
    DEGREE_180_REGEX,
    DEGREE_360_REGEX,
    DEGREE_SIGNED_90_REGEX,
    DMS_COORDINATE_REGEX,
    HM_TIME_REGEX,
    METADATA_REGEX,
    OPTIONAL_HM_TIME_REGEX,
)
from AstronomicalAnnualCalendar.utils import raw_delta_t_to_timedelta


@pytest.mark.parametrize(
    "time, hour, minute",
    [
        ("0h0m", "0", "0"),
        ("24h59m", "24", "59"),
        ("24h60m", "24", "60"),
        ("0h60m", "0", "60"),
    ],
)
def test_hh_time_regex(time: str, hour: str, minute: str):
    match: re.Match | None = HM_TIME_REGEX.match(time)
    assert isinstance(match, re.Match)
    assert match.string == time
    assert match.group("hour") == hour
    assert match.group("minute") == minute


@pytest.mark.parametrize(
    "time",
    [
        "0h 0m",
        "30h0m",
        "0h61m",
        "-",
        "-----",
    ],
)
def test_hh_time_regex_fail(time: str):
    assert HM_TIME_REGEX.match(time) is None


@pytest.mark.parametrize(
    "time, hour, minute",
    [
        ("0h0m", "0", "0"),
        ("24h59m", "24", "59"),
        ("24h60m", "24", "60"),
        ("0h60m", "0", "60"),
        ("-", None, None),
        ("-----", None, None),
    ],
)
def test_optional_hh_time_regex(time: str, hour: str | None, minute: str | None):
    match: re.Match | None = OPTIONAL_HM_TIME_REGEX.match(time)
    assert isinstance(match, re.Match)
    assert match.string == time
    assert match.group("hour") == hour
    assert match.group("minute") == minute


@pytest.mark.parametrize(
    "time",
    [
        "0h 0m",
        "30h0m",
        "0h61m",
    ],
)
def test_hh_optional_time_regex_fail(time: str):
    assert OPTIONAL_HM_TIME_REGEX.match(time) is None


@pytest.mark.parametrize(
    "angle, sign, degree",
    [
        ("+0°", "+", "0"),
        ("-0°", "-", "0"),
        ("+90°", "+", "90"),
        ("-90°", "-", "90"),
        ("+00°", "+", "00"),
        ("-00°", "-", "00"),
        ("+69°", "+", "69"),
        ("-69°", "-", "69"),
        ("+ 0°", "+", "0"),
        ("- 0°", "-", "0"),
        ("+ 90°", "+", "90"),
        ("- 90°", "-", "90"),
        ("+ 00°", "+", "00"),
        ("- 00°", "-", "00"),
        ("+ 69°", "+", "69"),
        ("- 69°", "-", "69"),
    ],
)
def test_degree_signed_90_regex_match(angle: str, sign: str, degree: str):
    match: re.Match | None = DEGREE_SIGNED_90_REGEX.match(angle)
    assert isinstance(match, re.Match)
    assert match.string == angle
    assert match.group("sign") == sign
    assert match.group("degree") == degree


@pytest.mark.parametrize(
    "angle, degree",
    [
        ("0°", "0"),
        ("00°", "00"),
        ("000°", "000"),
        ("100°", "100"),
        ("170°", "170"),
        ("179°", "179"),
        ("180°", "180"),
    ],
)
def test_degree_180_regex_match(angle: str, degree: str):
    match: re.Match | None = DEGREE_180_REGEX.match(angle)
    assert isinstance(match, re.Match)
    assert match.string == angle
    assert match.group("degree") == degree


@pytest.mark.parametrize(
    "angle, degree",
    [
        ("0°", "0"),
        ("00°", "00"),
        ("000°", "000"),
        ("100°", "100"),
        ("200°", "200"),
        ("300°", "300"),
        ("350°", "350"),
        ("359°", "359"),
        ("360°", "360"),
    ],
)
def test_degree_360_regex_match(angle: str, degree: str):
    match: re.Match | None = DEGREE_360_REGEX.match(angle)
    assert isinstance(match, re.Match)
    assert match.string == angle
    assert match.group("degree") == degree


@pytest.mark.parametrize(
    "coordinate, lat, lon",
    [
        ("53°05' N    7°25' O", "53°05' N", "7°25' O"),
        ("53°05' n    7°25' o", "53°05' n", "7°25' o"),
        ("53°05' S    7°25' O", "53°05' S", "7°25' O"),
        ("53°05' s    7°25' O", "53°05' s", "7°25' O"),
        ("53°05' S    7°25' E", "53°05' S", "7°25' E"),
        ("53°05' S    7°25' e", "53°05' S", "7°25' e"),
        ("53°05' S    7°25' E", "53°05' S", "7°25' E"),
        ("53°05' S    7°25' W", "53°05' S", "7°25' W"),
        ("53°05' S    7°25' w", "53°05' S", "7°25' w"),
        ("53°05' N 7°25' O", "53°05' N", "7°25' O"),
        ("53°05' N      7°25' O", "53°05' N", "7°25' O"),
        ("53°05' N,   7°25' O", "53°05' N", "7°25' O"),
        ("53°05' N ,  7°25' O", "53°05' N", "7°25' O"),
        ("53°05' N, 7°25' O", "53°05' N", "7°25' O"),
        ("53°05'N     7°25'O", "53°05'N", "7°25'O"),
        ("1°1'1\" N     1°1'1\" O", "1°1'1\" N", "1°1'1\" O"),
        ("1°1'1.1\" N     1°1'1.1\" O", "1°1'1.1\" N", "1°1'1.1\" O"),
        ("1°1'1.999999999\" N     1°1'1.999999999\" O", "1°1'1.999999999\" N", "1°1'1.999999999\" O"),
        ("1°1'1\"N     1°1'1\"O", "1°1'1\"N", "1°1'1\"O"),
        ("1°1'1.999999999\"N     1°1'1.999999999\"O", "1°1'1.999999999\"N", "1°1'1.999999999\"O"),
        ("333°22'22\" N     333°22'22\" O", "333°22'22\" N", "333°22'22\" O"),
    ],
)
def test_dms_coordinate_regex_match(coordinate: str, lat: str, lon: str):
    match: re.Match | None = DMS_COORDINATE_REGEX.match(coordinate)
    assert isinstance(match, re.Match)
    assert match.string == coordinate
    assert match.group("lat") == lat
    assert match.group("lon") == lon


@pytest.mark.parametrize(
    "coordinate",
    [
        "53°05' N7°25' O",
        "53°05' N,7°25' O",
        "53°05' N ,7°25' O",
        "53°05'X     7°25'O",
        "53°05'N     7°25'X",
        "°1'1.1\" N     1°1'1.1\" O",
        "1°'1.1\" N     1°1'1.1\" O",
        "1°1'.1\" N     1°1'1.1\" O",
        "1°1'1.\" N     1°1'1.1\" O",
        "1°1'1.1\" N     °1'1.1\" O",
        "1°1'1.1\" N     1°'1.1\" O",
        "1°1'1.1\" N     1°1'.1\" O",
        "1°1'1.1\" N     1°1'1.\" O",
        "4444°22'22\" N     333°22'22\" O",
        "333°333'22\" N     333°22'22\" O",
        "333°22'333\" N     333°22'22\" O",
        "333°22'22\" N     4444°22'22\" O",
        "333°22'22\" N     333°333'22\" O",
        "333°22'22\" N     333°22'333\" O",
    ],
)
def test_dms_coordinate_regex_fail(coordinate: str):
    assert DMS_COORDINATE_REGEX.match(coordinate) is None


@pytest.mark.parametrize(
    "coordinate, lat, lon",
    [
        ("53°05' N    7°25' O", "53°05' N", "7°25' O"),
        ("53°05' N 7°25' O", "53°05' N", "7°25' O"),
        ("53°05' N, 7°25' O", "53°05' N", "7°25' O"),
        ("53°05'N, 7°25'O", "53°05'N", "7°25'O"),
    ],
)
def test_dms_coordinate_regex_match_group_lat_lon(coordinate: str, lat: str, lon: str):
    match: re.Match = DMS_COORDINATE_REGEX.match(coordinate)
    assert match.group("lat") == lat
    assert match.group("lon") == lon


@pytest.mark.parametrize(
    "raw_metadata, place, coordinate, equinox, delta_t",
    [
        (
            "Ort: Papenburg,     53°05' N    7°25' O   Äquin:   2000.0, geozentrisch,  DeltaT = 73.9 s",
            "Papenburg",
            "53°05' N    7°25' O",
            2000.0,
            timedelta(seconds=73.9),
        ),
        (
            "Ort: Papenburg,     53°05' N    7°25' O   ,  DeltaT = 73.9 s",
            "Papenburg",
            "53°05' N    7°25' O",
            None,
            timedelta(seconds=73.9),
        ),
        (
            "Ort:Papenburg,53°05'N 7°25'O Äquin:0,geozentrisch,DeltaT=73s",
            "Papenburg",
            "53°05'N 7°25'O",
            0,
            timedelta(seconds=73),
        ),
        (
            "Ort: Papenburg,     53°05' N    7°25' O   Äquin:   -2000.0, geozentrisch,  DeltaT = -73.9 s",
            "Papenburg",
            "53°05' N    7°25' O",
            -2000.0,
            timedelta(seconds=-73.9),
        ),
        (
            "Ort: Santiago De Chile,     33°27' S   70°40' W   Äquin:   2000.0, geozentrisch,  DeltaT = 73.9 s",
            "Santiago De Chile",
            "33°27' S   70°40' W",
            2000.0,
            timedelta(seconds=73.9),
        ),
    ],
)
def test_metadata_regex_match(
    raw_metadata: str,
    place: str,
    coordinate: str,
    equinox: float | None,
    delta_t: timedelta,
):
    match: re.Match | None = METADATA_REGEX.match(raw_metadata)
    assert isinstance(match, re.Match)
    assert match.string == raw_metadata
    assert match.group("place") == place
    assert match.group("coordinate") == coordinate
    if equinox is None:
        assert match.group("equinox") == equinox
    else:
        assert float(match.group("equinox")) == equinox
    assert raw_delta_t_to_timedelta(match.group("delta_t"), match.group("delta_t_unit")) == delta_t
