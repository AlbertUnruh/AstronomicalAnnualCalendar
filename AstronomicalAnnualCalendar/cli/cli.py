# standard library
import logging
from contextvars import ContextVar

# third party
import click

# local
from ..flags import CLIFlags
from ..logger import get_logger
from ..translations import locale


__all__ = (
    "cli",
    "flags",
)


flags: ContextVar[CLIFlags] = ContextVar("flags", default=CLIFlags.DEFAULT)

get_logger("matplotlib").setLevel("INFO")  # suppress debug messages from matplotlib
logger = get_logger(None, add_handler=True)
_log_level: dict[CLIFlags, str] = {
    CLIFlags.SHOW_WARNINGS: "WARNING",
    CLIFlags.SHOW_INFOS: "INFO",
    CLIFlags.SHOW_DEBUG: "DEBUG",
    CLIFlags.QUIET: "CRITICAL",  # I know, it's not truly quiet...
}


@click.group()
@click.help_option()
@click.version_option()
@click.option(
    "--show-warnings",
    "-w",
    "verbosity",
    type=CLIFlags,
    flag_value=CLIFlags.SHOW_WARNINGS,
    default=CLIFlags.DEFAULT & CLIFlags.SHOW_WARNINGS,
)
@click.option(
    "--show-infos",
    "-i",
    "verbosity",
    type=CLIFlags,
    flag_value=CLIFlags.SHOW_INFOS,
    default=CLIFlags.DEFAULT & CLIFlags.SHOW_INFOS,
)
@click.option(
    "--show-debug",
    "-d",
    "verbosity",
    type=CLIFlags,
    flag_value=CLIFlags.SHOW_DEBUG,
    default=CLIFlags.DEFAULT & CLIFlags.SHOW_DEBUG,
)
@click.option(
    "--quiet",
    "-q",
    "verbosity",
    type=CLIFlags,
    flag_value=CLIFlags.QUIET,
    default=CLIFlags.DEFAULT & CLIFlags.QUIET,
)
@click.option(
    "--language",
    "-l",
    "lang",
    default=locale.get(),  # uses the default
    show_default=False,
    help="Sets the language for the command and media output.",
)
def cli(verbosity: CLIFlags, lang: str) -> None:
    _set_verbosity(verbosity)
    _set_language(lang)


def _set_verbosity(verbosity: CLIFlags) -> None:
    flags.set(flags.get() & ~CLIFlags.LOGGING_AND_VERBOSITY_FLAGS | verbosity)  # set verbosity

    for _logger in logging.root.manager.loggerDict.values():
        if not hasattr(_logger, "setLevel") or "matplotlib" in _logger.name:
            continue
        _logger.setLevel(_log_level[verbosity])

    logger.setLevel(_log_level[verbosity])
    logger.info(f"verbosity set to {verbosity.name}")


def _set_language(lang: str) -> None:
    logger.debug(f"using following language: {lang}")
    locale.set(lang)
