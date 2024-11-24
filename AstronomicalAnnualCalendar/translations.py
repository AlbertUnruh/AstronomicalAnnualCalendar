# standard library
import re
from collections.abc import Callable
from contextvars import ContextVar
from hashlib import sha1  # only used for key/id generation
from pathlib import Path

# first party
from AstronomicalAnnualCalendar.errors import TranslationsDirNotADirectoryError


__all__ = (
    "get_text",
    "locale",
)


locale: ContextVar[str] = ContextVar("locale", default="en")

_SHA1_MESSAGE_PAIRS_REGEX: re.Pattern[str] = re.compile(r"^(?P<sha1>[\da-f]{40}),\"(?P<message>.+)\"$", re.MULTILINE)


class _Translations:
    _translations_dir: Path
    _cached_translations: dict[str, dict[str, str]]  # {language: {sha1: message, ...}, ...}

    def __init__(self, translations_dir: Path):
        if not translations_dir.is_dir():
            raise TranslationsDirNotADirectoryError(translations_dir=translations_dir)
        self._translations_dir = translations_dir
        self._cached_translations = {}

    @property
    def translations_dir(self) -> Path:
        """Returns the directory for the translations."""
        return self._translations_dir

    def get_translations(self, *, lang: str | None = None) -> dict[str, str]:
        if lang is None:
            lang = locale.get()

        if lang not in self._cached_translations:
            translations: dict[str, str] = {}

            if (translation_file := self.translations_dir / f"{lang}.csv").is_file():
                for match in _SHA1_MESSAGE_PAIRS_REGEX.finditer(translation_file.read_text("utf-8")):
                    translations[match.group("sha1")] = match.group("message")

            self._cached_translations[lang] = translations

        return self._cached_translations[lang]

    def get_translation(self, message: str, *, lang: str | None = None) -> str | None:
        key: str = sha1(message.encode("utf-8")).hexdigest()  # noqa: S324
        return self.get_translations(lang=lang).get(key)

    def get_text(self, message: str, *, lang: str | None = None) -> str:
        """Find the translated message and return it if available (but defaults to the given input)."""
        return self.get_translation(message, lang=lang) or message


get_text: Callable[[str], str] = _Translations(Path(__file__).parent / Path("locales")).get_text
