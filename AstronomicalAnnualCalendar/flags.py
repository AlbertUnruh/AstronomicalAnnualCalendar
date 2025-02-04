# standard library
from functools import reduce
from operator import or_

# third party
from aenum import IntFlag, auto


__all__ = ("CLIFlags",)


class AntiIntFlag[T: int]:
    """Flag to represent a flag with the opposite value.

    Copied (and modified) from interactions.py [1] (interactions.models.discord.enums.AntiFlag).
    *interactions.py is licensed under the MIT License [2]*

    [1]: https://github.com/interactions-py/interactions.py/blob/83fef883471328deb322f1f2bfd66d937768876b/interactions/models/discord/enums.py#L60-L66
    [2]: https://github.com/interactions-py/interactions.py/blob/83fef883471328deb322f1f2bfd66d937768876b/LICENSE
    """

    def __init__(self, anti: T = 0) -> None:
        self.anti = anti

    def __get__(self, instance: IntFlag | None, cls) -> T:  # noqa: ANN001
        negative = ~cls(self.anti)
        return cls(reduce(or_, negative))


class CLIFlags(IntFlag):
    """A collection of flags that can be set via the CLI."""

    # logging/verbosity
    SHOW_WARNINGS = auto()
    SHOW_INFOS = auto()
    SHOW_DEBUG = auto()
    QUIET = auto()

    LOGGING_AND_VERBOSITY_FLAGS = SHOW_WARNINGS | SHOW_INFOS | SHOW_DEBUG | QUIET

    # specials
    NONE = 0
    ALL = AntiIntFlag(NONE)
    DEFAULT = SHOW_WARNINGS
