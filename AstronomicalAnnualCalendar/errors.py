__all__ = (
    "AstronomicalAnnualCalendarException",
    "UnitNotSupportedError",
)


class AstronomicalAnnualCalendarException(Exception):  # noqa: N818
    """Base exception for every custom exception and error produced by this project."""

    gh_message: str = (
        "Feel free to open a pull request over on [GitHub]"
        "(https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/issues)."
    )

    def __init__(self, message: str, /, *, gh: bool):
        info = " " + self.gh_message.strip() if gh else ""
        super().__init__(message + info)


class UnitNotSupportedError(AstronomicalAnnualCalendarException, NotImplementedError):
    """Error for ``utils.raw_delta_t_to_timedelta`` to signify, that an unknown unit was passed as a parameter."""

    def __init__(self, unit: str):
        super().__init__(f"The unit {unit!r} is not supported!", gh=True)
