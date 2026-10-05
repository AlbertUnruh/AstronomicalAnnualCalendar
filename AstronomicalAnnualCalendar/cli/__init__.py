# standard library
from pathlib import Path

# local
from . import cli as _cli  # preserve access to cli.py  # noqa: F401
from .cli import cli, flags

__all__ = ("cli", "flags")


# add all commands
for __file in Path(__file__).parent.iterdir():
    if __file.is_dir() or (__file.suffix != ".py") or ((__name := __file.stem) in ("__init__", "cli")):
        continue
    __import__(__name, globals(), {}, (), 1)
del __file, __name
