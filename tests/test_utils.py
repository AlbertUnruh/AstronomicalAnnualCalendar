# standard library
import re
from datetime import timedelta
from typing import Literal, SupportsFloat

# third party
import pytest

# first party
from AstronomicalAnnualCalendar.enums import ObservableObjectEnum
from AstronomicalAnnualCalendar.errors import AliasNotAssignedError, UnitNotSupportedError
from AstronomicalAnnualCalendar.models import ObservableObjectModel
from AstronomicalAnnualCalendar.utils import (
    append_name_to_all_pattern_groups,
    extract_pattern_from_regex,
    observable_object_from_alias,
    raw_delta_t_to_timedelta,
)


@pytest.mark.parametrize(
    "delta_t, unit, expected",
    [
        ("1", "s", timedelta(seconds=1)),
        ("1.0", "s", timedelta(seconds=1)),
        (1, "s", timedelta(seconds=1)),
        (1.0, "s", timedelta(seconds=1)),
    ],
)
def test_raw_delta_t_to_timedelta(delta_t: SupportsFloat, unit: Literal["s"], expected: timedelta):
    assert raw_delta_t_to_timedelta(delta_t, unit) == expected


@pytest.mark.parametrize(
    "delta_t, unit, error",
    [
        (1, "m", UnitNotSupportedError),
        (1, "h", UnitNotSupportedError),
        (1, "ms", UnitNotSupportedError),
        (1, "us", UnitNotSupportedError),
        ("one", "s", ValueError),
    ],
)
def test_raw_delta_t_to_timedelta_fail(delta_t: SupportsFloat, unit: str, error: BaseException):
    with pytest.raises(error):  # type: ignore
        raw_delta_t_to_timedelta(delta_t, unit)  # type: ignore[literal-required]


@pytest.mark.parametrize(
    "pattern, expected",
    [
        (r"", r""),
        (r"^", r""),
        (r"$", r""),
        (r"^$", r""),
        (rb"", rb""),
        (rb"^", rb""),
        (rb"$", rb""),
        (rb"^$", rb""),
    ],
)
def test_extract_pattern_from_regex[T: str | bytes](pattern: T, expected: T):
    assert extract_pattern_from_regex(re.compile(pattern)) == expected


@pytest.mark.parametrize(
    "pattern, name, expected",
    [
        # A regex to check for a's
        ("a+", "", "a+"),
        ("a+", "_xyz", "a+"),
        ("(a+)", "_xyz", "(a+)"),
        ("(?P<a>a+)", "", "(?P<a>a+)"),
        ("(?P<a>a+)", "_xyz", "(?P<a_xyz>a+)"),
        ("(?P<a>a+)", "_XYZ", "(?P<a_XYZ>a+)"),
        (b"a+", b"", b"a+"),
        (b"a+", b"_xyz", b"a+"),
        (b"(a+)", b"_xyz", b"(a+)"),
        (b"(?P<a>a+)", b"", b"(?P<a>a+)"),
        (b"(?P<a>a+)", b"_xyz", b"(?P<a_xyz>a+)"),
        (b"(?P<a>a+)", b"_XYZ", b"(?P<a_XYZ>a+)"),
        # A regex to check for a's and then b's
        ("a+b+", "", "a+b+"),
        ("a+b+", "_xyz", "a+b+"),
        ("(a+)(b+)", "_xyz", "(a+)(b+)"),
        ("(?P<a>a+)(?P<b>b+)", "", "(?P<a>a+)(?P<b>b+)"),
        ("(?P<a>a+)(?P<b>b+)", "_xyz", "(?P<a_xyz>a+)(?P<b_xyz>b+)"),
        ("(?P<a>a+)(?P<b>b+)", "_XYZ", "(?P<a_XYZ>a+)(?P<b_XYZ>b+)"),
        (b"a+b+", b"", b"a+b+"),
        (b"a+b+", b"_xyz", b"a+b+"),
        (b"(a+)(b+)", b"_xyz", b"(a+)(b+)"),
        (b"(?P<a>a+)(?P<b>b+)", b"", b"(?P<a>a+)(?P<b>b+)"),
        (b"(?P<a>a+)(?P<b>b+)", b"_xyz", b"(?P<a_xyz>a+)(?P<b_xyz>b+)"),
        (b"(?P<a>a+)(?P<b>b+)", b"_XYZ", b"(?P<a_XYZ>a+)(?P<b_XYZ>b+)"),
        # Something a bit more complicated now...
        (
            r"^(?P<hour>[01]?\d|2[0-3])h(?P<minute>[0-5]\d)m(?P<second>[0-5]\d(\.\d+)?)s$",
            "",
            r"^(?P<hour>[01]?\d|2[0-3])h(?P<minute>[0-5]\d)m(?P<second>[0-5]\d(\.\d+)?)s$",
        ),
        (
            r"^(?P<hour>[01]?\d|2[0-3])h(?P<minute>[0-5]\d)m(?P<second>[0-5]\d(\.\d+)?)s$",
            "_",
            r"^(?P<hour_>[01]?\d|2[0-3])h(?P<minute_>[0-5]\d)m(?P<second_>[0-5]\d(\.\d+)?)s$",
        ),
        (
            rb"^(?P<hour>[01]?\d|2[0-3])h(?P<minute>[0-5]\d)m(?P<second>[0-5]\d(\.\d+)?)s$",
            b"",
            rb"^(?P<hour>[01]?\d|2[0-3])h(?P<minute>[0-5]\d)m(?P<second>[0-5]\d(\.\d+)?)s$",
        ),
        (
            rb"^(?P<hour>[01]?\d|2[0-3])h(?P<minute>[0-5]\d)m(?P<second>[0-5]\d(\.\d+)?)s$",
            b"_",
            rb"^(?P<hour_>[01]?\d|2[0-3])h(?P<minute_>[0-5]\d)m(?P<second_>[0-5]\d(\.\d+)?)s$",
        ),
    ],
)
def test_append_name_to_all_pattern_groups[T: str | bytes](pattern: T, name: T, expected: T):
    assert append_name_to_all_pattern_groups(name, pattern) == expected


@pytest.mark.parametrize(
    "alias, expected",
    [
        # by id
        ("sun", ObservableObjectEnum.SUN),
        ("mercury", ObservableObjectEnum.MERCURY),
        ("venus", ObservableObjectEnum.VENUS),
        ("moon", ObservableObjectEnum.MOON),
        ("mars", ObservableObjectEnum.MARS),
        ("jupiter", ObservableObjectEnum.JUPITER),
        ("saturn", ObservableObjectEnum.SATURN),
        ("uranus", ObservableObjectEnum.URANUS),
        ("neptune", ObservableObjectEnum.NEPTUNE),
        # by alias
        ("Sonne", ObservableObjectEnum.SUN),
        ("Merkur", ObservableObjectEnum.MERCURY),
        ("Venus", ObservableObjectEnum.VENUS),
        ("Mond", ObservableObjectEnum.MOON),
        ("Mars", ObservableObjectEnum.MARS),
        ("Jupiter", ObservableObjectEnum.JUPITER),
        ("Saturn", ObservableObjectEnum.SATURN),
        ("Uranus", ObservableObjectEnum.URANUS),
        ("Neptun", ObservableObjectEnum.NEPTUNE),
    ],
)
def test_observable_object_from_alias(alias: str, expected: ObservableObjectModel):
    model = observable_object_from_alias(alias)
    assert isinstance(model, ObservableObjectModel)
    assert model == expected


@pytest.mark.parametrize(
    "alias",
    ["SUN", "MERCURY", "VENUS", "MOON", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE"],
)
def test_observable_object_from_alias_fail(alias: str):
    with pytest.raises(AliasNotAssignedError):
        observable_object_from_alias(alias)
