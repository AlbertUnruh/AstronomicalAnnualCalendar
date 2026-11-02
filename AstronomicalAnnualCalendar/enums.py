# standard library
import re

# third party
from aenum import EnumMeta, NoAliasEnum, UniqueEnum
from pydantic_extra_types.color import Color

# local
from .models import HeaderModel as HModel
from .models import ObservableObjectModel as OOModel

__all__ = (
    "HeaderEnum",
    "ObservableObjectEnum",
)


class DirectValueMeta(EnumMeta):
    """Metaclass to allow direct access to an enum-members value without the need to call ``.value`` beforehand."""

    def __getattribute__[T](cls, name: str) -> T:  # noqa: N805
        """Return ``.value.<name>`` after the enum-member is fully initialized."""
        value = super().__getattribute__(name)
        if isinstance(value, cls):  # if it's an Enum-class
            value = value.value
        return value


class ObservableObjectEnum(NoAliasEnum, metaclass=DirectValueMeta):
    """
    For every object to be included in the calendar.

    Lists the sun and every planet in the solar system (except planet earth as calculation is based on this planet).

    Currently, it includes the moon as an experimental feature as the source of inspiration [1] for this project
    excludes it.

    [1]: https://sternwarte-papenburg.de/jahreskalender/download/ajk_2024.pdf
    *in case the download gets removed: https://web.archive.org/web/20240531110805/https://sternwarte-papenburg.de/jahreskalender/download/ajk_2024.pdf
    """

    SUN = OOModel(id="sun", aliases={"Sonne"}, line_color=Color("#ea7500"))
    MERCURY = OOModel(id="mercury", aliases={"Merkur"}, line_color=Color("#333333"))
    VENUS = OOModel(id="venus", aliases={"Venus"}, line_color=Color("#00cc00"))
    MOON = OOModel(id="moon", aliases={"Mond"}, line_color=Color("seagreen"))
    # ^^^ EXPERIMENTAL; may get excluded if it's to wonky ^^^
    MARS = OOModel(id="mars", aliases={"Mars"}, line_color=Color("#ff0000"))
    JUPITER = OOModel(id="jupiter", aliases={"Jupiter"}, line_color=Color("#0000ff"))
    SATURN = OOModel(id="saturn", aliases={"Saturn"}, line_color=Color("#ff33ff"))
    URANUS = OOModel(id="uranus", aliases={"Uranus"}, line_color=Color("#99ccff"))
    # ^^^ rename to "Urectum" in 2620 (https://futurama.fandom.com/wiki/Urectum) ^^^
    NEPTUNE = OOModel(id="neptune", aliases={"Neptun"}, line_color=Color("#cc994a"))


class HeaderEnum(UniqueEnum, metaclass=DirectValueMeta):
    """
    An enum to store every header that may be present in the observable object's data.

    Members contain regex to find their position (and offsets if needed) to obtain the desired information.
    """

    WEEKDAY = HModel(name="weekday", regex=re.compile(r"^ {2}(?= {4})"), length=2)
    DATE = HModel(name="date", regex=re.compile(r"Datum"), length=10, offset=2)
    TIME = HModel(name="time", regex=re.compile(r"MEZ |MESZ|UTC "), length=8, offset=2)
    # space after "MEZ" and "UTC" required to obtain a total length of 4 for the match
    CULMINATION = HModel(name="culmination", regex=re.compile(r"Kulm\."), length=6)
