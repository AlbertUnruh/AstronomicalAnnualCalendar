# standard library
from pathlib import Path
from typing import TYPE_CHECKING

# third party
import click

# local
from ..generator import generate_and_save_explanation, generate_and_save_graph
from ..logger import get_logger
from ..parser import AstroWinParser
from ..translations import get_text as _
from ..utils import format_to_wh, merge_pdfs
from . import cli

if TYPE_CHECKING:
    # local
    from ..models import DataModel, ObservableObjectModel


__all__ = ("generate",)


logger = get_logger("generate@cli")


@cli.command(help="Generate the astronomical annual calendar.")
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
    help="The title may include '%s' for the place to be filled in by metadata.",
)
@click.option(
    "--format",
    "-f",
    "fmt",
    type=str,
    default="A4",
    help="The desired format for the output. May be 'A4' or 'A3'. For landscape append 'h'.",
)
@click.option(
    "--explanation-format",
    "-ef",
    "explanation_format",
    type=str,
    default="A4",
    help="The desired format for the explanation. May be 'A4' or 'A3'. For landscape append 'h'.",
)
def generate(source: Path, destination: Path, title: str | None, fmt: str, explanation_format: str):
    logger.info(f"reading data from {source.resolve()}")
    parser = AstroWinParser(file_path=source)
    data: dict[ObservableObjectModel, DataModel] = parser.parse()

    is_overwriting = destination.is_file()
    is_pdf = destination.suffix == ".pdf"

    size = format_to_wh(fmt)
    explanation_destination = destination.with_stem(f"{destination.stem}-explanation")

    generate_and_save_graph(data=data, destination=destination, title=title, size=size)
    generate_and_save_explanation(destination=explanation_destination, size=format_to_wh(explanation_format))

    if is_pdf:
        merge_pdfs(destination, explanation_destination, destination=destination)
        explanation_destination.unlink()

    logger.debug(f"output written to {destination.resolve()}{" (overwriting)" * is_overwriting}")
    if not is_pdf:
        logger.debug(f"explanation written to {explanation_destination.resolve()}{" (overwriting)" * is_overwriting}")

    click.secho(_("Output written to %s") % destination, fg="blue")
    if not is_pdf:
        click.secho(_("Explanation written to %s") % explanation_destination, fg="cyan")

    click.secho(_("Enjoy your astronomical calendar!"), fg="bright_green")
