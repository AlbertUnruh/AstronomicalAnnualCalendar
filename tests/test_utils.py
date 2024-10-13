# standard library
import re
from datetime import timedelta
from typing import Literal, SupportsFloat

# third party
import pytest

# first party
from AstronomicalAnnualCalendar.errors import UnitNotSupportedError
from AstronomicalAnnualCalendar.utils import extract_pattern_from_regex, raw_delta_t_to_timedelta


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
