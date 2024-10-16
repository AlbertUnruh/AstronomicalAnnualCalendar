# standard library
from contextvars import ContextVar

# local
from .enums import Flags


__all__ = ("flags",)


flags: ContextVar[Flags] = ContextVar("flags", default=Flags.DEFAULT)
