# standard library
from pathlib import Path
from typing import TYPE_CHECKING

# third party
import click

# local
from ..generator import generate_and_save_graph
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
@click.option(
    "--title",
    "-t",
    "title",
    type=str,
    default=None,
    help="The title may include '%s' for the place to be filled in by metadata",
)
def generate(source: Path, destination: Path, title: str | None):
    logger.info(f"reading data from {source.resolve()}")
    parser = Parser(file_path=source)
    data: dict[ObservableObjectModel, DataModel] = parser.parse()

    is_overwriting = destination.is_file()

    generate_and_save_graph(data=data, destination=destination, title=title)

    logger.debug(f"output written to {destination.resolve()}{" (overwriting)" * is_overwriting}")
    click.secho(_("Output written to %s") % destination, fg="blue")
    click.secho(_("Enjoy your astronomical calendar!"), fg="bright_green")
    logger.warning("Graph alignment not final!")
