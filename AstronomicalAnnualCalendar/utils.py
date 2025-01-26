# standard library
import re
import sys
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from typing import Literal, SupportsFloat

# third party
from click import get_current_context
from pydantic import ValidationError
from pypdf import PdfReader, PdfWriter

# local
from . import __repository__, __version__
from .errors import (
    AliasNotAssignedError,
    MalformedPaperFormatError,
    UnitNotSupportedError,
    UnknownPaperFormatError,
    UnknownPaperOrientationError,
)
from .logger import get_logger
from .translations import get_text as _
from .translations import locale


# I'm fully aware that the following try-except is a war-crime, but this was the easiest solution I could think of...
# Should you have a better solution please open a pull-request over on GitHub
# (https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/pulls)
# ~AlbertUnruh

try:  # pragma: no cover
    """
    The following imports will raise an ImportError due to circular imports.
    I still import them to get type-hints support from the IDE.
    """

    # local
    from .enums import HeaderEnum, ObservableObjectEnum
    from .models import EvaluatedHeaderModel, ObservableObjectModel

    def _fix_imports():
        pass

except ImportError:
    EvaluatedHeaderModel = None
    HeaderEnum = None
    ObservableObjectModel = None
    ObservableObjectEnum = None

    def _fix_imports():
        global EvaluatedHeaderModel, HeaderEnum, ObservableObjectModel, ObservableObjectEnum, _fix_imports  # noqa: PLW0603
        # local
        from .enums import HeaderEnum, ObservableObjectEnum
        from .models import EvaluatedHeaderModel, ObservableObjectModel

        logger.debug("imports in utils.py are now fixed")

        def _fix_imports():
            pass


__all__ = (
    "append_name_to_all_pattern_groups",
    "extract_pattern_from_regex",
    "format_to_wh",
    "generate_metadata",
    "get_aac_title",
    "get_present_headers",
    "issue19_note_on_validation_error",
    "merge_pdfs",
    "observable_object_from_alias",
    "optional_hm_str_to_timedelta",
    "raw_delta_t_to_timedelta",
)


logger = get_logger("utils@core")

_PREFIX: dict[type, str | bytes] = {str: "^", bytes: b"^"}
_SUFFIX: dict[type, str | bytes] = {str: "$", bytes: b"$"}
_NAME_PATTERN: dict[type, str | bytes] = {str: r"\?P<(?P<name>\w+)>", bytes: rb"\?P<(?P<name>\w+)>"}
_NAME_PREFIX: dict[type, str | bytes] = {str: "?P<", bytes: b"?P<"}
_NAME_SUFFIX: dict[type, str | bytes] = {str: ">", bytes: b">"}


def extract_pattern_from_regex[T: str | bytes](regex: re.Pattern[T], /) -> T:
    """Extract pattern from re.Pattern ^ and $ before returning it."""
    pattern = regex.pattern
    t_ = type(pattern)
    return pattern.removeprefix(_PREFIX[t_]).removesuffix(_SUFFIX[t_])


def append_name_to_all_pattern_groups[T: str | bytes](name: T, pattern: T) -> T:
    """
    Append ``name`` to every named capturing group in the given ``pattern``.

    It's recommended to prepend "_" to the ``name``.
    """
    t_ = type(pattern)

    def create_name(match: re.Match[T]) -> T:
        return t_().join(
            [
                _NAME_PREFIX[t_],
                match.group("name"),  # doesn't need to be bytes if T is bytes
                name,
                _NAME_SUFFIX[t_],
            ]
        )

    return re.sub(_NAME_PATTERN[t_], create_name, pattern)


def raw_delta_t_to_timedelta(delta_t: SupportsFloat, unit: Literal["s"]) -> timedelta:
    """Convert DeltaT (raw metadata) to a timedelta-object."""
    delta_t: float = float(delta_t)
    match unit:
        case "s":  # seconds
            return timedelta(seconds=delta_t)
        case _:
            raise UnitNotSupportedError(unit)


def observable_object_from_alias(alias: str) -> ObservableObjectModel:
    """Retrieve desired ObservableObjectModel based on a given alias."""
    _fix_imports()
    model: ObservableObjectModel
    aliases: set[str]
    for model, aliases in [(e.value, e.value.aliases) for e in ObservableObjectEnum]:  # type: ignore
        if alias in aliases:
            return model
    raise AliasNotAssignedError(alias)


def get_present_headers(bound_object: ObservableObjectModel, header: str) -> list[EvaluatedHeaderModel]:
    """Retrieve every header that is present in the given header."""
    _fix_imports()
    return [
        EvaluatedHeaderModel(bound_object=bound_object, bound_header=enum.value, endpos=match.span()[1])
        for enum in HeaderEnum  # type: ignore
        if (match := enum.value.search(header)) is not None
    ]


@contextmanager
def issue19_note_on_validation_error():
    """Small contextmanager to apply a note for any `ValidationError`s raised."""
    try:
        yield
    except ValidationError as e:
        e.add_note(
            _("For more information on the exception follow [this](%s) link.")
            % "https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/issues/19"
        )
        raise


def optional_hm_str_to_timedelta(hm: str | None) -> timedelta | None:
    """Get timedelta from ``HHhMMm`` formatted string (with HH being ``0``-``24`` and MM being ``-9``-``60``)."""
    if hm is None or len(hm) * "-" == hm:
        return None
    return timedelta(hours=int(hm[:-4]), minutes=int(hm[-3:-1]))


def generate_metadata(title: str) -> dict:
    """Generate metadata for generated files."""
    py_v = ".".join(str(getattr(sys.version_info, part)) for part in ("major", "minor", "micro"))
    aac_v = __version__
    pkg = __package__
    repo = __repository__
    lang = locale.get().upper()
    cmd = ctx.command.name if (ctx := get_current_context(silent=True)) else "*function*"
    metadata = {
        "Title": title,
        "Creator": f"{pkg} v{aac_v}, {repo}",
        "Producer": f"{pkg} --language {lang} {cmd} ({aac_v}/py{py_v})",
    }
    logger.debug("metadata:")
    for entry, value in metadata.items():
        logger.debug(f"  - {entry:9} {value}")
    return metadata


def get_aac_title(title: str | None, place: str) -> str:
    """Get a title for the astronomical annual calendar."""
    if title is None:
        title = _("astronomical annual calendar for %s")
    if "%s" in title:
        title = title % place
    return title


def format_to_wh(format: str) -> tuple[float, float]:  # noqa: A002
    """Return size of format as width/height tuple (in inches)."""
    match len(format):
        case 2:
            orientation = "v"  # default
            size = format
        case 3:
            orientation = format[-1]
            size = format[:2]
        case __:
            raise MalformedPaperFormatError(format)

    if orientation not in ("v", "h"):
        raise UnknownPaperOrientationError(orientation, format)

    ret: tuple[float, float]
    match size.upper():
        case "A0":
            ret = (33.1102362205, 46.8110236220)
        case "A1":
            ret = (23.3858267717, 33.1102362205)
        case "A2":
            ret = (16.5354330709, 23.3858267717)
        case "A3":
            ret = (11.6929133858, 16.5354330709)
        case "A4":
            ret = (8.2677165354, 11.6929133858)
        case __:
            raise UnknownPaperFormatError(format, biggest="A0", smallest="A4")

    return ret if orientation == "v" else ret[::-1]


def merge_pdfs(*pdfs: Path, destination: Path):
    """Merge multiple pdfs into one big pdf at the given destination."""
    with PdfWriter(str(destination.resolve())) as merger:
        merger.add_metadata(PdfReader(pdfs[0]).metadata)
        for pdf in pdfs:
            merger.append(pdf)
