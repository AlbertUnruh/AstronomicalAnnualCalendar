# standard library
import re
from datetime import timedelta
from typing import Literal, SupportsFloat

# local
from .errors import UnitNotSupportedError


__all__ = (
    "extract_pattern_from_regex",
    "raw_delta_t_to_timedelta",
)


_PREFIX: dict[type, str | bytes] = {str: "^", bytes: b"^"}
_SUFFIX: dict[type, str | bytes] = {str: "$", bytes: b"$"}


def extract_pattern_from_regex[T: (str, bytes)](regex: re.Pattern[T], /) -> T:
    """Extract pattern from re.Pattern ^ and $ before returning it."""
    pattern = regex.pattern
    t_ = type(pattern)
    return pattern.removeprefix(_PREFIX[t_]).removesuffix(_SUFFIX[t_])


def raw_delta_t_to_timedelta(delta_t: SupportsFloat, unit: Literal["s"]) -> timedelta:
    """Convert DeltaT (raw metadata) to a timedelta-object."""
    delta_t: float = float(delta_t)
    match unit:
        case "s":  # seconds
            return timedelta(seconds=delta_t)
        case _:
            raise UnitNotSupportedError(unit)
