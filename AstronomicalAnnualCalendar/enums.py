# standard library
from functools import reduce
from operator import or_

# third party
from aenum import EnumMeta, IntFlag, NoAliasEnum, auto
from pydantic_extra_types.color import Color

# local
from .models import ObservableObjectModel


__all__ = (
    "ObservableObjectEnum",
    "Flags",
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

    SUN: ObservableObjectModel = ObservableObjectModel(id="sun", line_color=Color("orange"))
    MERCURY: ObservableObjectModel = ObservableObjectModel(id="mercury", line_color=Color("black"))
    VENUS: ObservableObjectModel = ObservableObjectModel(id="venus", line_color=Color("green"))
    MOON: ObservableObjectModel = ObservableObjectModel(id="moon", line_color=Color("violet"))
    # ^^^ EXPERIMENTAL; may get excluded if it's to wonky ^^^
    MARS: ObservableObjectModel = ObservableObjectModel(id="mars", line_color=Color("red"))
    JUPITER: ObservableObjectModel = ObservableObjectModel(id="jupiter", line_color=Color("blue"))
    SATURN: ObservableObjectModel = ObservableObjectModel(id="saturn", line_color=Color("pink"))
    URANUS: ObservableObjectModel = ObservableObjectModel(id="uranus", line_color=Color("turquoise"))
    # ^^^ rename to "Urectum" in 2620 (https://futurama.fandom.com/wiki/Urectum) ^^^
    NEPTUNE: ObservableObjectModel = ObservableObjectModel(id="neptune", line_color=Color("gold"))


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


class Flags(IntFlag):
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
