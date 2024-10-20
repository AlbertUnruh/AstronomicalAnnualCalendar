# standard library
from contextvars import ContextVar

# local
from .enums import CLIFlags


__all__ = ("flags",)


flags: ContextVar[CLIFlags] = ContextVar("flags", default=CLIFlags.DEFAULT)
