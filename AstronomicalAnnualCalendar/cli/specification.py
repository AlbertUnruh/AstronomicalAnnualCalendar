# standard library
from collections.abc import Callable

# third party
import click
from click import Command

# local
from ..logger import get_logger
from ..parser import get_all_parsers
from ..parser._base import ABCParser
from .cli import cli

__all__ = ("specification",)


logger = get_logger("specification@cli")


specification = cli.group(help="List available commands for the specifications", name="specification")(type(None))


def parser_spec(parser: type[ABCParser]) -> Callable[[], None]:
    def command():
        click.secho(parser.specification)

    return command


for _p in get_all_parsers():
    name = _p.parser_name
    # logger.debug(f"Adding sub-command {name!r}")
    specification.add_command(Command(name=name, callback=parser_spec(_p), help=f"Display specifications for {name}"))
