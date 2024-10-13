# standard library
import re

# local
from .utils import extract_pattern_from_regex


__all__ = (
    "DMS_COORDINATE_REGEX",
    "METADATA_REGEX",
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
    r"^(?P<lat>(\d{1,3})°(\d{1,2})'(\d{1,2}(\.\d+)?)?\"?\s?([%s]))(\s*,\s*)?\s+(?P<lon>(\d{1,3})°(\d{1,2})'(\d{1,2}(\.\d+)?)?\"?\s?([%s]))$"  # noqa: UP031
    % ("".join(_ALLOWED_LAT), "".join(_ALLOWED_LON)),
    flags=re.IGNORECASE,
)

METADATA_REGEX: re.Pattern[str] = re.compile(
    r"^Ort:\s*(?P<place>[^,]+),\s*(?P<coordinate>%s)\s*(\sÄquin:\s*(?P<equinox>-?\d+(\.\d+)?),\s*geozentrisch)?,\s*DeltaT\s?=\s?(?P<delta_t>-?\d+(\.\d+)?)\s?(?P<delta_t_unit>\w+)$"  # noqa: UP031
    % extract_pattern_from_regex(DMS_COORDINATE_REGEX),
    flags=re.IGNORECASE | re.MULTILINE,
)
