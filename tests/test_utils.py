# standard library
import re
from datetime import timedelta
from pathlib import Path
from typing import Literal, SupportsFloat

# third party
import pytest
from pydantic import ValidationError

# first party
from AstronomicalAnnualCalendar.enums import ObservableObjectEnum
from AstronomicalAnnualCalendar.errors import (
    AliasNotAssignedError,
    MalformedPaperFormatError,
    UnitNotSupportedError,
    UnknownPaperFormatError,
    UnknownPaperOrientationError,
)
from AstronomicalAnnualCalendar.models import ObservableObjectModel
from AstronomicalAnnualCalendar.translations import locale
from AstronomicalAnnualCalendar.utils import (
    append_name_to_all_pattern_groups,
    extract_pattern_from_regex,
    format_to_wh,
    issue19_note_on_validation_error,
    merge_pdfs,
    observable_object_from_alias,
    optional_hm_str_to_timedelta,
    raw_delta_t_to_timedelta,
)


@pytest.mark.parametrize(
    ("delta_t", "unit", "expected"),
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
    ("delta_t", "unit", "error"),
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
    ("pattern", "expected"),
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
    ("pattern", "name", "expected"),
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
    ("alias", "expected"),
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


@pytest.mark.parametrize(
    ("hm", "expected"),
    [
        (None, None),
        ("", None),
        ("-", None),
        ("------", None),
        ("00h00m", timedelta(hours=0, minutes=0)),
        ("0h00m", timedelta(hours=0, minutes=0)),
        ("00h99m", timedelta(hours=0, minutes=99)),
        ("99h00m", timedelta(hours=99, minutes=0)),
        ("9h00m", timedelta(hours=9, minutes=0)),
    ],
)
def test_optional_hm_str_to_timedelta(hm: str | None, expected: timedelta | None):
    assert optional_hm_str_to_timedelta(hm) == expected


@pytest.mark.parametrize(
    ("fmt", "expected"),
    [
        ("A0", (33.110, 46.811)),
        ("A1", (23.386, 33.110)),
        ("A2", (16.535, 23.386)),
        ("A3", (11.693, 16.535)),
        ("A4", (8.268, 11.693)),
        ("a4", (8.268, 11.693)),  # if lowercase works for A4, it'll work everywhere
    ],
)
def test_format_to_wh(fmt: str, expected: tuple[float, float]):
    tol = 0.001
    assert len(fmt) == 2  # noqa: PLR2004
    assert format_to_wh(fmt) == pytest.approx(expected, abs=tol)
    assert format_to_wh(fmt + "v") == pytest.approx(expected, abs=tol)
    assert format_to_wh(fmt + "h") == pytest.approx(expected[::-1], abs=tol)


@pytest.mark.parametrize(
    ("fmt", "exception"),
    [
        ("", MalformedPaperFormatError),
        ("A", MalformedPaperFormatError),
        ("A4H", UnknownPaperOrientationError),
        ("A4V", UnknownPaperOrientationError),
        ("A4q", UnknownPaperOrientationError),
        ("A5", UnknownPaperFormatError),
        ("B0", UnknownPaperFormatError),
    ],
)
def test_format_to_wh_fail(fmt: str, exception: type[Exception]):
    with pytest.raises(exception):
        format_to_wh(fmt)


def test_issue19_note_on_validation_error():
    locale.set("en")
    issue19 = re.compile(r"https://github\.com/AlbertUnruh/AstronomicalAnnualCalendar/issues/19")
    with pytest.raises(ValidationError, match=issue19), issue19_note_on_validation_error():
        raise ValidationError("test", [])


@pytest.mark.parametrize("use_first_pdf_as_destination", [False, True])
@pytest.mark.parametrize(
    ("pdf_path_fixtures", "expected_pdf_path_fixture"),
    [
        (["path_test_0_pdf", "path_test_1_pdf"], "path_test_expected_pdf"),
    ],
)
def test_merge_pdfs(
    use_first_pdf_as_destination: bool,
    pdf_path_fixtures: list[str],
    expected_pdf_path_fixture: str,
    tmp_path: Path,
    request: pytest.FixtureRequest,
):
    pdfs: list[Path] = [request.getfixturevalue(pdf_path_fixture) for pdf_path_fixture in pdf_path_fixtures]
    destination = tmp_path / "out.pdf"
    expected_pdf_path: Path = request.getfixturevalue(expected_pdf_path_fixture)

    if use_first_pdf_as_destination:
        destination.write_bytes(pdfs[0].read_bytes())  # copy contents of first PDF to `destination`
        pdfs[0] = destination  # set `destination` as first PDF

    merge_pdfs(*pdfs, destination=destination)

    # expected_pdf = PdfReader(expected_pdf_path)
    # actual_pdf = PdfReader(destination)

    # assert actual_pdf.metadata == expected_pdf.metadata
    # assert actual_pdf.get_num_pages() == expected_pdf.get_num_pages()

    assert destination.read_bytes() == expected_pdf_path.read_bytes()  # very strict
