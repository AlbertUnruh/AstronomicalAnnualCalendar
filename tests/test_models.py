# standard library
from datetime import UTC, datetime, timedelta
from functools import partial

# third party
import pytest
from pydantic_core import ValidationError
from pydantic_extra_types.color import Color

# first party
from AstronomicalAnnualCalendar import models
from AstronomicalAnnualCalendar.models import ObservableObjectModel, RowModel
from tests.typehints import GetTextCallable


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
    ("oom", "expected"),
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
    ("oom", "expected"),
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
    ("oom", "expected"),
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


@pytest.mark.parametrize(
    ("lang", "oom", "expected"),
    [
        ("en", ObservableObjectModel(id="id #1", line_color=Color("000")), "id number one"),
        ("en", ObservableObjectModel(id="id #2", line_color=Color("000")), "id number two"),
        ("de", ObservableObjectModel(id="id #1", line_color=Color("000")), "ID Nummer eins"),
        ("de", ObservableObjectModel(id="id #2", line_color=Color("000")), "ID Nummer zwei"),
    ],
)
def test_oom_localized_name(lang: str, oom: ObservableObjectModel, expected: str, get_text: GetTextCallable):
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(models, "get_text", partial(get_text, lang=lang))  # use test-translations
        assert oom.name == expected


@pytest.mark.parametrize(
    ("date_and_time", "bound_object"),
    [
        (datetime.now(UTC), ObservableObjectModel(id="row_model_test", line_color=Color("000"))),
    ],
)
@pytest.mark.parametrize(
    ("culmination", "expected_culmination"),
    [
        ("0h00m", timedelta(hours=0, minutes=0)),
        ("00h00m", timedelta(hours=0, minutes=0)),
        ("24h00m", timedelta(hours=24, minutes=0)),
        ("12h34m", timedelta(hours=12, minutes=34)),
        ("00h-1m", timedelta(hours=0, minutes=-1)),
        (_td := timedelta(), _td),
        (_td := timedelta(hours=0, minutes=0), _td),
        (_td := timedelta(hours=24, minutes=0), _td),
        (_td := timedelta(hours=12, minutes=34), _td),
        (_td := timedelta(hours=0, minutes=-1), _td),
    ],
)
def test_row_model(
    date_and_time: datetime,
    bound_object: ObservableObjectModel,
    culmination: str | timedelta,
    expected_culmination: timedelta,
):
    row = RowModel(bound_object=bound_object, date_and_time=date_and_time, culmination=culmination)
    assert row.bound_object == bound_object
    assert row.date_and_time == date_and_time
    assert row.culmination == expected_culmination
