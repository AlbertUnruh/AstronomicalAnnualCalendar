# standard library
import re
from datetime import timedelta
from typing import Literal, SupportsFloat

# local
from .errors import AliasNotAssignedError, UnitNotSupportedError


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
    from .enums import ObservableObjectEnum
    from .models import ObservableObjectModel

    def _fix_imports():
        pass

except ImportError:
    ObservableObjectModel = None
    ObservableObjectEnum = None

    def _fix_imports():
        global ObservableObjectModel, ObservableObjectEnum, _fix_imports
        # local
        from .enums import ObservableObjectEnum
        from .models import ObservableObjectModel

        def _fix_imports():
            pass


__all__ = (
    "extract_pattern_from_regex",
    "append_name_to_all_pattern_groups",
    "raw_delta_t_to_timedelta",
    "observable_object_from_alias",
)


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
