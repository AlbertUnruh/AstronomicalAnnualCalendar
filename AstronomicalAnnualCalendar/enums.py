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
    RIGHT_ASCENSION = HModel(name="right_ascension", regex=re.compile(r"Rektasz\."), length=11)
    DECLINATION = HModel(name="declination", regex=re.compile(r"Deklin\."), length=10)
    ECLIPTIC_LONGITUDE = HModel(name="ecliptic_longitude", regex=re.compile(r"Ekl\. Lg\."), length=10)
    ECLIPTIC_LATITUDE = HModel(name="ecliptic_latitude", regex=re.compile(r"Ekl\. Br"), length=10)
    RISE = HModel(name="rise", regex=re.compile(r"Aufg\."), length=6)
    CULMINATION = HModel(name="culmination", regex=re.compile(r"Kulm\."), length=6)
    SET = HModel(name="set", regex=re.compile(r"Unterg"), length=6)
    AZIMUT_RIZE = HModel(name="azimut_rise", regex=re.compile(r"(?<=Az )Auf"), length=4)
    AZIMUT_SET = HModel(name="azimut_set", regex=re.compile(r"(?<=Az Auf )Unt\."), length=4)
    DISTANCE = HModel(name="distance", regex=re.compile(r"Entf\."), length=8, offset=1)
    BRIGHTNESS = HModel(name="brightness", regex=re.compile(r"Hell\."), length=5)
    DIAMETER = HModel(name="diameter", regex=re.compile(r"Ø \[\"]"), length=6)
    DIAMETER_RING = HModel(name="diameter_ring", regex=re.compile(r"Ø Ring"), length=4)
    DAWN = HModel(name="dawn", regex=re.compile(r"ADämm"), length=6)
    DUSK = HModel(name="dusk", regex=re.compile(r"EDämm"), length=6)
    PHASE = HModel(name="phase", regex=re.compile(r"Phase"), length=5)
    AGE = HModel(name="age", regex=re.compile(r"Alter"), length=5)
    ELONGATION = HModel(name="elongation", regex=re.compile(r"Elong"), length=6)

    # following attribute-names aren't worked out yet -> they may get deprecated and replaced
    # *see AstronomicalAnnualCalendar.models.RowModel for more
    PHAS_W = HModel(name="phas_w", regex=re.compile(r"Phas\.W\."), length=6)
    PHYSICAL_EPHEMERIS__NP__OR__PA_N = HModel(
        name="physical_ephemeris__np__or__pa_n", regex=re.compile(r"Pos\.W\."), length=6
    )
    PHYSICAL_EPHEMERIS__SEP_DELTA = HModel(name="physical_ephemeris__sep_delta", regex=re.compile(r"BrErde"), length=6)
    PHYSICAL_EPHEMERIS__SEP_OMEGA = HModel(
        name="physical_ephemeris__sep_omega", regex=re.compile(r"ZM"), length=5, offset=1
    )
    MOON_SPECIFIC_LIB_LONGITUDE = HModel(
        name="moon_specific_lib_longitude", regex=re.compile(r"Lib Lg\."), length=4, offset=-1
    )
    MOON_SPECIFIC_LIB_LATITUDE = HModel(
        name="moon_specific_lib_latitude", regex=re.compile(r"(?<=Lib Lg\. {2})Br\."), length=4
    )
    MOON_SPECIFIC_COLONG = HModel(name="moon_specific_colong", regex=re.compile(r"Colong\."), length=5)
    MOON_SPECIFIC_BR = HModel(name="moon_specific_br", regex=re.compile(r"(?<=Colong\. {2})Br\."), length=4)
