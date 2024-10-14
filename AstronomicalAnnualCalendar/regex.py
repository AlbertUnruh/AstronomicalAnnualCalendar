# standard library
import re

# local
from .utils import append_name_to_all_pattern_groups, extract_pattern_from_regex


__all__ = (
    "HMS_ANGLE_REGEX",
    "DMS_ANGLE_90_REGEX",
    "DMS_ANGLE_360_REGEX",
    "DMS_COORDINATE_REGEX",
    "METADATA_REGEX",
)


HMS_ANGLE_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<hour>[01]?\d|2[0-3])h(?P<minute>[0-5]\d)m(?P<second>[0-5]\d(\.\d+)?)s$",
    flags=re.IGNORECASE,
)

DMS_ANGLE_90_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<sign>[+\-])(?P<degree>[0-8 ]?\d|90)°((?P<minute>\s?([0-5 ])?\d)'(\s?(?P<second>(([0-5 ])?\d|60)(\.\d+)?)\")?)?$",  # noqa: E501
    flags=re.IGNORECASE,
)

DMS_ANGLE_360_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<degree>[0-2 ]?[\d ]?\d|3[0-5]\d|360)°((?P<minute>\s?([0-5 ])?\d)'(\s?(?P<second>(([0-5 ])?\d|60)(\.\d+)?)\")?)?$",  # noqa: E501
    flags=re.IGNORECASE,
)


_ALLOWED_LAT = frozenset[str](
    [
        "N",  # EN: north; DE: Norden
        "S",  # EN: south; DE: Süden
    ]
)
_ALLOWED_LON = frozenset[str](
    [
        "W",  # EN: west; DE: Westen
        "E",  # EN: east
        "O",  # DE: Osten
    ]
)

DMS_COORDINATE_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<lat>(%s\s?([%s])))(\s*,\s*)?\s+(?P<lon>(%s\s?([%s])))$"  # noqa: UP031
    % (
        append_name_to_all_pattern_groups("_lat", extract_pattern_from_regex(DMS_ANGLE_360_REGEX)),
        "".join(_ALLOWED_LAT),
        append_name_to_all_pattern_groups("_lon", extract_pattern_from_regex(DMS_ANGLE_360_REGEX)),
        "".join(_ALLOWED_LON),
    ),
    flags=re.IGNORECASE,
)

METADATA_REGEX: re.Pattern[str] = re.compile(
    r"^Ort:\s*(?P<place>[^,]+),\s*(?P<coordinate>%s)\s*(\sÄquin:\s*(?P<equinox>-?\d+(\.\d+)?),\s*geozentrisch)?,\s*DeltaT\s?=\s?(?P<delta_t>-?\d+(\.\d+)?)\s?(?P<delta_t_unit>\w+)$"  # noqa: UP031
    % extract_pattern_from_regex(DMS_COORDINATE_REGEX),
    flags=re.IGNORECASE | re.MULTILINE,
)
