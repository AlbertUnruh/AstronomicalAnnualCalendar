# third party
import pytest
from pydantic_core import ValidationError
from pydantic_extra_types.color import Color

# first party
from AstronomicalAnnualCalendar.models import ObservableObjectModel


def test_oom_internal_id():
    oom = ObservableObjectModel(id="oom", line_color=Color("000"))
    assert oom != "oom"
    assert oom.internal_id == "oom"

    with pytest.raises(ValidationError):
        ObservableObjectModel(id="OOM", line_color=Color("000"))


def test_oom_name():
    oom = ObservableObjectModel(id="oom", line_color=Color("000"))
    assert oom.name == oom.internal_id == "oom"


@pytest.mark.parametrize(
    "oom, expected",
    [
        (ObservableObjectModel(id="oom", line_color=Color("000")), False),
        (ObservableObjectModel(id="oom", line_color=Color("000"), is_sun=False), False),
        (ObservableObjectModel(id="oom", line_color=Color("000"), is_sun=True), True),
        (ObservableObjectModel(id="sun", line_color=Color("000")), True),
        (ObservableObjectModel(id="sun", line_color=Color("000"), is_sun=False), False),
        (ObservableObjectModel(id="sun", line_color=Color("000"), is_sun=True), True),
        (ObservableObjectModel(id="sunny", line_color=Color("000")), False),
    ],
)
def test_oom_is_sun(oom: ObservableObjectModel, expected: bool):
    assert oom.is_sun == expected


@pytest.mark.parametrize(
    "oom, expected",
    [
        (ObservableObjectModel(id="oom", line_color=Color("000")), False),
        (ObservableObjectModel(id="oom", line_color=Color("000"), is_moon=False), False),
        (ObservableObjectModel(id="oom", line_color=Color("000"), is_moon=True), True),
        (ObservableObjectModel(id="moon", line_color=Color("000")), True),
        (ObservableObjectModel(id="moon", line_color=Color("000"), is_moon=False), False),
        (ObservableObjectModel(id="moon", line_color=Color("000"), is_moon=True), True),
        (ObservableObjectModel(id="moonshine", line_color=Color("000")), False),
    ],
)
def test_oom_is_moon(oom: ObservableObjectModel, expected: bool):
    assert oom.is_moon == expected


@pytest.mark.parametrize(
    "oom, expected",
    [
        (ObservableObjectModel(id="oom", line_color=Color("000")), True),
        (ObservableObjectModel(id="oom", line_color=Color("000"), is_planet=False), False),
        (ObservableObjectModel(id="oom", line_color=Color("000"), is_planet=True), True),
        (ObservableObjectModel(id="planet", line_color=Color("000")), True),
        (ObservableObjectModel(id="sun", line_color=Color("000")), False),
        (ObservableObjectModel(id="moon", line_color=Color("000")), False),
        (ObservableObjectModel(id="planet", line_color=Color("000"), is_planet=False), False),
        (ObservableObjectModel(id="planet", line_color=Color("000"), is_planet=True), True),
        (ObservableObjectModel(id="planet", line_color=Color("000"), is_sun=True), False),
        (ObservableObjectModel(id="planet", line_color=Color("000"), is_moon=True), False),
        (ObservableObjectModel(id="planetarium", line_color=Color("000")), True),
        (ObservableObjectModel(id="something", line_color=Color("000")), True),
    ],
)
def test_oom_is_planet(oom: ObservableObjectModel, expected: bool):
    assert oom.is_planet == expected
