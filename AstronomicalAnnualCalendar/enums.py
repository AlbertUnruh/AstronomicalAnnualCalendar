# standard library
import re
from functools import reduce
from operator import or_

# third party
from aenum import EnumMeta, IntFlag, NoAliasEnum, UniqueEnum, auto
from pydantic_extra_types.color import Color

# local
from .models import HeaderModel as HModel
from .models import ObservableObjectModel as OOModel


__all__ = (
    "ObservableObjectEnum",
    "CLIFlags",
    "HeaderEnum",
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

    SUN: OOModel = OOModel(id="sun", aliases={"Sonne"}, line_color=Color("orange"))
    MERCURY: OOModel = OOModel(id="mercury", aliases={"Merkur"}, line_color=Color("black"))
    VENUS: OOModel = OOModel(id="venus", aliases={"Venus"}, line_color=Color("green"))
    MOON: OOModel = OOModel(id="moon", aliases={"Mond"}, line_color=Color("violet"))
    # ^^^ EXPERIMENTAL; may get excluded if it's to wonky ^^^
    MARS: OOModel = OOModel(id="mars", aliases={"Mars"}, line_color=Color("red"))
    JUPITER: OOModel = OOModel(id="jupiter", aliases={"Jupiter"}, line_color=Color("blue"))
    SATURN: OOModel = OOModel(id="saturn", aliases={"Saturn"}, line_color=Color("pink"))
    URANUS: OOModel = OOModel(id="uranus", aliases={"Uranus"}, line_color=Color("turquoise"))
    # ^^^ rename to "Urectum" in 2620 (https://futurama.fandom.com/wiki/Urectum) ^^^
    NEPTUNE: OOModel = OOModel(id="neptune", aliases={"Neptun"}, line_color=Color("gold"))


class HeaderEnum(UniqueEnum):
    """
    An enum to store every header that may be present in the observable object's data.

    Members contain regex to find their position (and offsets if needed) to obtain the desired information.
    """

    WEEKDAY: HModel = HModel(regex=re.compile(r"^ {2}(?= {4})"), length=2)
    DATE: HModel = HModel(regex=re.compile(r"Datum"), length=10, offset=2)
    TIMEZONE: HModel = HModel(regex=re.compile(r"MEZ |MESZ|UTC "), length=8, offset=2)
    # space after "MEZ" and "UTC" required to obtain a total length of 4 for the match
    RIGHT_ASCENSION: HModel = HModel(regex=re.compile(r"Rektasz\."), length=11)
    DECLINATION: HModel = HModel(regex=re.compile(r"Deklin\."), length=10)
    ECLIPTIC_LONGITUDE: HModel = HModel(regex=re.compile(r"Ekl\. Lg\."), length=10)
    ECLIPTIC_LATITUDE: HModel = HModel(regex=re.compile(r"Ekl\. Br"), length=10)
    RISE: HModel = HModel(regex=re.compile(r"Aufg\."), length=6)
    CULMINATION: HModel = HModel(regex=re.compile(r"Kulm\."), length=6)
    SET: HModel = HModel(regex=re.compile(r"Unterg"), length=6)
    AZIMUT_RIZE: HModel = HModel(regex=re.compile(r"(?<=Az )Auf"), length=4)
    AZIMUT_SET: HModel = HModel(regex=re.compile(r"(?<=Az Auf )Unt\."), length=4)
    DISTANCE: HModel = HModel(regex=re.compile(r"Entf\."), length=8, offset=1)
    BRIGHTNESS: HModel = HModel(regex=re.compile(r"Hell\."), length=5)
    DIAMETER: HModel = HModel(regex=re.compile(r"Ø \[\"]"), length=6)
    DAWN: HModel = HModel(regex=re.compile(r"ADämm"), length=6)
    DUSK: HModel = HModel(regex=re.compile(r"EDämm"), length=6)
    PHASE: HModel = HModel(regex=re.compile(r"Phase"), length=5)
    AGE: HModel = HModel(regex=re.compile(r"Alter"), length=5)
    ELONGATION: HModel = HModel(regex=re.compile(r"Elong"), length=6)

    # following attribute-names aren't worked out yet -> they may get deprecated and replaced
    # *see AstronomicalAnnualCalendar.models.RowModel for more
    PHAS_W: HModel = HModel(regex=re.compile(r"Phas\.W\."), length=6)
    PHYSICAL_EPHEMERIS__NP__OR__PA_N: HModel = HModel(regex=re.compile(r"Pos\.W\."), length=6)
    PHYSICAL_EPHEMERIS__SEP_DELTA: HModel = HModel(regex=re.compile(r"BrErde"), length=6)
    PHYSICAL_EPHEMERIS__SEP_OMEGA: HModel = HModel(regex=re.compile(r"ZM"), length=5, offset=1)
    MOON_SPECIFIC_LIB_LONGITUDE: HModel = HModel(regex=re.compile(r"Lib Lg\."), length=4, offset=-1)
    MOON_SPECIFIC_LIB_LATITUDE: HModel = HModel(regex=re.compile(r"(?<=Lib Lg\. {2})Br\."), length=4)
    MOON_SPECIFIC_COLONG: HModel = HModel(regex=re.compile(r"Colong\."), length=5)
    MOON_SPECIFIC_BR: HModel = HModel(regex=re.compile(r"(?<=Colong\. {2})Br\."), length=4)


class AntiIntFlag[T: int]:
    """Flag to represent a flag with the opposite value.

    Copied (and modified) from interactions.py [1] (interactions.models.discord.enums.AntiFlag).
    *interactions.py is licensed under the MIT license [2]*

    [1]: https://github.com/interactions-py/interactions.py/blob/83fef883471328deb322f1f2bfd66d937768876b/interactions/models/discord/enums.py#L60-L66
    [2]: https://github.com/interactions-py/interactions.py/blob/83fef883471328deb322f1f2bfd66d937768876b/LICENSE
    """

    def __init__(self, anti: T = 0) -> None:
        self.anti = anti

    def __get__(self, instance: IntFlag | None, cls: EnumMeta) -> T:
        negative = ~cls(self.anti)
        return cls(reduce(or_, negative))


class CLIFlags(IntFlag):
    """A collection of flags that can be set via the CLI."""

    # cli
    INTERACTIVE = auto()

    # logging/verbosity
    SHOW_WARNINGS = auto()
    SHOW_INFOS = auto()
    SHOW_DEBUG = auto()
    QUIET = auto()

    # info included in AAC
    DISPLAY_PLACE = auto()
    DISPLAY_COORDINATE = auto()
    DISPLAY_EQUINOX = auto()
    DISPLAY_DELTA_T = auto()

    # ToDo: complete flags

    # specials
    NONE = 0
    ALL = AntiIntFlag(NONE)
    DEFAULT = INTERACTIVE | SHOW_WARNINGS | DISPLAY_PLACE  # ToDo: update as flags get added
