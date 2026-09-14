# modified copy of
# https://github.com/AlbertUnruh/AlbertUnruhUtils.py/blob/18f075888227b5cecfa385d86b7c721c17c79570/AlbertUnruhUtils/utils/logger.py

# standard library
import sys
import typing
from logging import Formatter, Logger, StreamHandler, getLogger

__all__ = ("get_logger",)


class ColorStr(str):
    def format(self, *args: ..., **kwargs: ...) -> str:
        level: int = kwargs.get("levelno", 0)
        if level >= 50:  # noqa: PLR2004
            color_code = "30;47;1"  # CRITICAL/FATAL
        elif level >= 40:  # noqa: PLR2004
            color_code = "31;1"  # ERROR
        elif level >= 30:  # noqa: PLR2004
            color_code = "35"  # WARNING
        elif level >= 20:  # noqa: PLR2004
            color_code = "36"  # INFO
        elif level >= 10:  # noqa: PLR2004
            color_code = "32"  # DEBUG
        else:
            color_code = "33;102"  # unknown
        return super().replace("COLOR-CODE", color_code).format(*args, **kwargs)


_LOG_LEVEL_STR = typing.Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]
_F = ColorStr("\033[COLOR-CODEm{asctime} \t{name: <15} {levelname: <10}\t{message}\033[0m")
_logging_formatter = Formatter(_F, style="{")
_logging_handler = StreamHandler(sys.stdout)
_logging_handler.setFormatter(_logging_formatter)


def get_logger(  # noqa: D103
    name: str | None, *, level: _LOG_LEVEL_STR | int | None = "DEBUG", add_handler: bool = False
) -> Logger:
    logger = getLogger(name)
    if add_handler:
        logger.addHandler(_logging_handler)
    if level is not None:
        if isinstance(level, str):
            level = level.upper()
        logger.setLevel(level)
    return logger
