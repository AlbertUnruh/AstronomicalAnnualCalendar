# standard library
from typing import TypeVar

# third party
from aenum import EnumMeta, NoAliasEnum
from pydantic_extra_types.color import Color

# local
from .models import ObservableObjectModel


__all__ = ("ObservableObjectEnum",)


T = TypeVar("T")


class DirectValueMeta(EnumMeta):
    """Metaclass to allow direct access to an enum-members value without the need to call ``.value`` beforehand."""

    def __getattribute__(cls, name: str) -> T:  # noqa: N805
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
    *in case the download gets removed:  TODO: add link from archive.org
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
    #  ^^^ rename to "Urectum" in 2620 (https://futurama.fandom.com/wiki/Urectum) ^^^
    NEPTUNE: ObservableObjectModel = ObservableObjectModel(id="neptune", line_color=Color("gold"))
