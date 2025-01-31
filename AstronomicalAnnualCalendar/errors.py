# standard library
from pathlib import Path


__all__ = (
    "AliasNotAssignedError",
    "AstronomicalAnnualCalendarException",
    "EvaluatedHeaderValidationError",
    "MalformedPaperFormatError",
    "PaperFormatError",
    "TranslationsDirNotADirectoryError",
    "UnitNotSupportedError",
    "UnknownPaperFormatError",
    "UnknownPaperOrientationError",
)


class AstronomicalAnnualCalendarException(Exception):  # noqa: N818
    """Base exception for every custom exception and error produced by this project."""

    gh_message: str = (
        "Feel free to open a pull request over on [GitHub]"
        "(https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/issues)."
    )

    def __init__(self, message: str, /, *, gh: bool = False):
        info = " " + self.gh_message.strip() if gh else ""
        super().__init__(message + info)


class UnitNotSupportedError(AstronomicalAnnualCalendarException, NotImplementedError):
    """
    Error for ``utils.raw_delta_t_to_timedelta``.

    It's used to signify that an unknown unit was passed as a parameter.
    """

    def __init__(self, unit: str):
        super().__init__(f"The unit {unit!r} is not supported!", gh=True)


class AliasNotAssignedError(AstronomicalAnnualCalendarException, ValueError):
    """
    Error for ``utils.observable_object_from_alias``.

    It's used to signify that an unknown alias was passed to look up an ObservableObjectModel.
    """

    def __init__(self, alias: str):
        super().__init__(f"The alias {alias!r} is not set for any `ObservableObjectModel`", gh=True)


class EvaluatedHeaderValidationError(AstronomicalAnnualCalendarException, ValueError):
    """Error for ``models.EvaluatedHeaderModel``."""

    def __init__(self, *, endpos: int, offset: int, length: int, startpos: int):
        super().__init__(
            f"The combination of `endpos` ({endpos}) and retrieved `offset` ({offset}) and "
            f"`length` ({length}) is invalid! Starting index would be {startpos}!"
        )


class TranslationsDirNotADirectoryError(AstronomicalAnnualCalendarException, ValueError, NotADirectoryError):
    """Error for ``translations._Translations``."""

    def __init__(self, *, translations_dir: Path):
        super().__init__(
            f"The path {translations_dir.as_posix()} is not a directory! "
            f"A directory is required as translations are stored in separate files!"
        )


class PaperFormatError(AstronomicalAnnualCalendarException, ValueError):
    """Base exception for ``utils.format_to_wh``."""


class MalformedPaperFormatError(PaperFormatError):
    """Error for ``utils.format_to_wh``."""

    def __init__(self, fmt: str):
        super().__init__(f"Malformed paper format {fmt!r}. Length should be 2 or 3 and not {len(fmt)}!")


class UnknownPaperOrientationError(PaperFormatError):
    """Error for ``utils.format_to_wh``."""

    def __init__(self, orientation: str, fmt: str):
        super().__init__(
            f"Unknown orientation {orientation!r} detected from {fmt!r}. "
            f"Expecting 'v' (vertical/portrait) or 'h' (horizontal/landscape)!"
        )


class UnknownPaperFormatError(PaperFormatError):
    """Error for ``utils.format_to_wh``."""

    def __init__(self, fmt: str, *, biggest: str, smallest: str):
        super().__init__(f"Unknown format {fmt!r}! {biggest!r} to {smallest!r} supported!")
