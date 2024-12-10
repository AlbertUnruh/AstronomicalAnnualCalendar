# standard library
from contextvars import ContextVar

# local
from .flags import CLIFlags


__all__ = ("flags",)


flags: ContextVar[CLIFlags] = ContextVar("flags", default=CLIFlags.DEFAULT)
