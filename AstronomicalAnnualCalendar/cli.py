# standard library
from contextvars import ContextVar
from json import load
from typing import TYPE_CHECKING
from urllib.error import HTTPError
from urllib.request import urlopen

# third party
import click

# local
from .flags import CLIFlags
from .translations import get_text as _
from .translations import locale


if TYPE_CHECKING:
    # standard library
    from http.client import HTTPResponse


__all__ = (
    "cli",
    "flags",
)


flags: ContextVar[CLIFlags] = ContextVar("flags", default=CLIFlags.DEFAULT)


@click.group()
@click.help_option()
@click.version_option()
@click.option(
    "--language",
    "-l",
    "lang",
    default=locale.get(),  # uses the default
    show_default=False,
    help="Sets the language for the command and media output.",
)
def cli(lang: str) -> None:  # noqa: D103
    locale.set(lang)


@cli.command(help="Displays version info (current/latest)")
def info():
    package = __import__(__package__)

    repository: str = package.__repository__.rstrip("/").split("/")[-2:]
    latest_release_url: str = f"https://api.github.com/repos/{repository[0]}/{repository[1]}/releases/latest"

    current_version: str = package.__version__
    latest_version: str

    try:
        response: HTTPResponse = urlopen(latest_release_url)  # noqa: S310
    except HTTPError as e:
        latest_version = "0.0.0"
        click.secho(_("Unable to load latest release-data from GitHub..."), err=True, fg="red")
        if e.code == 404:  # noqa: PLR2004
            click.secho(_("Are you using this project as an early bird? -> nothing released yet..."), fg="magenta")
    else:
        latest_version = load(response)["tag_name"].lstrip("v")

    click.secho(_("Current version: %s") % current_version, fg="blue")
    click.secho(_("Latest version:  %s") % latest_version, fg="blue")

    cv: tuple[str, ...] = tuple(current_version.split())
    lv: tuple[str, ...] = tuple(latest_version.split())

    message: str
    style: dict[str, ...] = {}

    if lv > cv:
        message = _("A new update is available!")
        style["fg"] = "bright_red"
    elif lv == cv:
        message = _("You have the latest version installed.")
        style["fg"] = "bright_green"
    else:  # lv < cv
        message = _("Wait, are you currently developing?")
        style["fg"] = "bright_yellow"

    click.secho(message, **style)
