# standard library
from collections.abc import Callable
from contextvars import ContextVar
from pathlib import Path

# first party
from AstronomicalAnnualCalendar.errors import TranslationsDirNotADirectoryError


__all__ = ("get_text",)

locale: ContextVar[str] = ContextVar("locale", default="en")


class _Translations:
    def __init__(self, translations_dir: Path):
        if not translations_dir.is_dir():
            raise TranslationsDirNotADirectoryError(translations_dir=translations_dir)
        self._translations_dir = translations_dir

    @property
    def translations_dir(self) -> Path:
        """Returns the directory for the translations."""
        return self._translations_dir

    def get_translations(self) -> dict[str, str]:
        return {}

    def get_text(self, message: str) -> str:
        """Find the translated message and return it if available (but defaults to the given input)."""
        translations: dict[str, str] = self.get_translations()
        return translations.get(message) or message


get_text: Callable[[str], str] = _Translations(Path(__file__).parent / "locales").get_text
