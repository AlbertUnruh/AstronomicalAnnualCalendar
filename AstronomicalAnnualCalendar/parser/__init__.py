# local
from ._base import ABCParser
from .astrowin import AstroWinParser


__all__ = ("AstroWinParser", "get_all_parsers")


def get_all_parsers[T: type[ABCParser]](*, base: T = ABCParser) -> list[T]:
    """Gather every parser that inherits from the base-parser and return them."""
    return base.__subclasses__()  # as simple as that (:
