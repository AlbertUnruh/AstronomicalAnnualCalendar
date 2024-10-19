# standard library
import re

# local
from .utils import append_name_to_all_pattern_groups, extract_pattern_from_regex


__all__ = (
    "HM_TIME_REGEX",
    "OPTIONAL_HM_TIME_REGEX",
    "DEGREE_SIGNED_90_REGEX",
    "DEGREE_180_REGEX",
    "DEGREE_360_REGEX",
    "HMS_ANGLE_REGEX",
    "DMS_ANGLE_90_REGEX",
    "DMS_ANGLE_360_REGEX",
    "DMS_COORDINATE_REGEX",
    "METADATA_REGEX",
    "OBJECT_DATA_BODY_REGEX",
)


HM_TIME_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<hour>[01]?\d|2[0-3]|24)h(?P<minute>[0-5]?\d|60)m$",
    # 60 minutes only allowed for edge-cases.
    # Even though this isn't the case for 2024 I want to be future-proof about that.
    flags=re.IGNORECASE,
)

OPTIONAL_HM_TIME_REGEX: re.Pattern[str] = re.compile(
    r"^(%s|-+)$" % extract_pattern_from_regex(HM_TIME_REGEX),
    flags=re.IGNORECASE,
)

DEGREE_SIGNED_90_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<sign>[+\-])\s*(?P<degree>[0-8]?\d|90)°$",
    flags=re.IGNORECASE,
)

DEGREE_180_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<degree>\d{1,2}|[01][0-7]\d|180)°$",
    flags=re.IGNORECASE,
)

DEGREE_360_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<degree>\d{1,2}|[0-2]\d{2}|3[0-5]\d|360)°$",
    flags=re.IGNORECASE,
)

HMS_ANGLE_REGEX: re.Pattern[str] = re.compile(
    r"^%s(?P<second>[0-5]\d(\.\d+)?)s$" % extract_pattern_from_regex(HM_TIME_REGEX),
    flags=re.IGNORECASE,
)

_DMS_ANGLE_MS_PART: str = r"((?P<minute>\s?([0-5 ])?\d)'(\s?(?P<second>(([0-5 ])?\d|60)(\.\d+)?)\")?)?"

DMS_ANGLE_90_REGEX: re.Pattern[str] = re.compile(
    r"^%s%s$"
    % (
        extract_pattern_from_regex(DEGREE_SIGNED_90_REGEX),
        _DMS_ANGLE_MS_PART,
    ),
    flags=re.IGNORECASE,
)

DMS_ANGLE_360_REGEX: re.Pattern[str] = re.compile(
    r"^%s%s$"
    % (
        extract_pattern_from_regex(DEGREE_360_REGEX),
        _DMS_ANGLE_MS_PART,
    ),
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
    r"^(?P<lat>(%s\s?([%s])))(\s*,\s*)?\s+(?P<lon>(%s\s?([%s])))$"
    % (
        append_name_to_all_pattern_groups("_lat", extract_pattern_from_regex(DMS_ANGLE_360_REGEX)),
        "".join(_ALLOWED_LAT),
        append_name_to_all_pattern_groups("_lon", extract_pattern_from_regex(DMS_ANGLE_360_REGEX)),
        "".join(_ALLOWED_LON),
    ),
    flags=re.IGNORECASE,
)

METADATA_REGEX: re.Pattern[str] = re.compile(
    r"^Ort:\s*(?P<place>[^,]+),\s*(?P<coordinate>%s)\s*(\sÄquin:\s*(?P<equinox>-?\d+(\.\d+)?),\s*geozentrisch)?,\s*DeltaT\s?=\s?(?P<delta_t>-?\d+(\.\d+)?)\s?(?P<delta_t_unit>\w+)$"
    % extract_pattern_from_regex(DMS_COORDINATE_REGEX),
    flags=re.IGNORECASE | re.MULTILINE,
)

OBJECT_DATA_BODY_REGEX: re.Pattern[str] = re.compile(
    r"^(?P<name>\S+)\n(?P<header>[^\n]+)\n(?P<body>([\s\S]*?(?=\n$)))",
    flags=re.MULTILINE,
)  # the text requires a new-line ("\n") at the end of the input data/text
