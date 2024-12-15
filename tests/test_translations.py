# standard library
from pathlib import Path

# third party
import pytest

# first party
from AstronomicalAnnualCalendar import translations
from AstronomicalAnnualCalendar.errors import TranslationsDirNotADirectoryError

# local
from .typehints import GetTextCallable


def test_fail_on_not_a_directory():
    with pytest.raises(TranslationsDirNotADirectoryError):
        translations._Translations(Path(__file__))  # noqa: SLF001


_translations: list[tuple[str, str, str]] = [  # locale/lang, message, expected
    # en
    ("en", "Hello, World!", "Hello, World!"),
    ("en", "Test with single 'quotes'", "Test with single 'quotes'"),
    ("en", 'Test with double "quotes"', 'Test with double "quotes"'),
    # de
    ("de", "Hello, World!", "Hallo, Welt!"),
    ("de", "Test with single 'quotes'", "Test mit einfachen 'Anführungszeichen'"),
    ("de", 'Test with double "quotes"', 'Test mit doppelten "Anführungszeichen"'),
]


@pytest.mark.parametrize(("locale", "message", "expected"), _translations)
def test_locale(get_text: GetTextCallable, locale: str, message: str, expected: str):
    translations.locale.set(locale)
    assert get_text(message) == expected


@pytest.mark.parametrize(("lang", "message", "expected"), _translations)
def test_lang(get_text: GetTextCallable, lang: str, message: str, expected: str):
    assert get_text(message, lang=lang) == expected


@pytest.mark.parametrize(
    ("lang", "message"),
    [
        ("de", "Not translated in `de`"),
        ("unknown locale", __import__("secrets").token_urlsafe()),  # can't be translated beforehand :D
    ],
)
def test_message_not_translated(get_text: GetTextCallable, lang: str, message: str):
    assert get_text(message, lang=lang) == message
