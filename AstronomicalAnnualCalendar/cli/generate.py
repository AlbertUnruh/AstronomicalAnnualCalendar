# standard library
from pathlib import Path

# third party
import click

# local
from ..logger import get_logger
from . import cli


__all__ = ("generate",)


logger = get_logger("generate@cli")


@cli.command(help="Generate the astronomical annual calendar")
@click.option(
    "--source",
    "-s",
    "source",
    type=click.File("r"),
)
@click.option(
    "--destination",
    "-d",
    "destination",
    type=click.Path(dir_okay=False, path_type=Path),
)
def generate(source: click.File, destination: click.File):
    pass
