# standard library
from pathlib import Path
from typing import TYPE_CHECKING

# third party
import click

# local
from ..logger import get_logger
from ..parser import Parser
from ..translations import get_text as _
from . import cli


if TYPE_CHECKING:
    # local
    from ..models import DataModel, ObservableObjectModel


__all__ = ("generate",)


logger = get_logger("generate@cli")


@cli.command(help="Generate the astronomical annual calendar")
@click.option(
    "--source",
    "-s",
    "source",
    type=click.Path(dir_okay=False, readable=True, path_type=Path),
    required=True,
)
@click.option(
    "--destination",
    "-d",
    "destination",
    type=click.Path(dir_okay=False, path_type=Path),
    required=True,
)
def generate(source: Path, destination: Path):
    logger.info(f"reading data from {source.resolve()}")
    parser = Parser(file_path=source)
    data: dict[ObservableObjectModel, DataModel] = parser.parse()  # noqa: F841

    logger.critical("Data not processed yet!")
    logger.critical("Nothing will be saved!")

    logger.debug(f"writing output to {destination.resolve()}{" (overriding)" * destination.is_file()}")
    click.secho(_("Writing output to %s") % destination, fg="blue")

    click.secho(_("Enjoy your astronomical calendar!"), fg="bright_green")
