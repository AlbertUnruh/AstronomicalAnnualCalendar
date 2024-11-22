# standard library
import re
from collections.abc import Iterable
from difflib import Differ
from hashlib import sha1  # only used for key/id generation
from logging import basicConfig, debug, info
from pathlib import Path


#
# logging
#
basicConfig(format="{asctime} \t{name: <10} {levelname: <10}\t{message}", style="{", level="DEBUG", encoding="utf-8")


#
# paths
#
AAC_PATH: Path = Path(__file__).parent / "AstronomicalAnnualCalendar"
LOCALES_PATH: Path = AAC_PATH / "locales"
TEMPLATE_FILE: Path = LOCALES_PATH / "template.csv"

if not LOCALES_PATH.is_dir():
    LOCALES_PATH.mkdir()


#
# find translatable messages
#
def iter_files(_dir: Path, suffix: str) -> Iterable[Path]:
    """Recursively iter over every .py-file in the given directory."""
    for path in _dir.iterdir():
        if path.is_dir():
            yield from iter_files(path, suffix)
        elif path.suffix == suffix:
            yield path


messages: set[str] = {
    # they are all known but accessed translated via attribute --> not mentioned in ``get_text()`` or ``_()``
    "sun",
    "mercury",
    "venus",
    "moon",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
}
debug(f"Following messages are pre-set: {", ".join(sorted(messages))}")

GETTEXT_RE: re.Pattern[str] = re.compile(r"(get_text|_)\(([\"\'])(?P<message>.+)\2\)")

for file in iter_files(AAC_PATH, ".py"):
    info(f"Searching in {file.as_posix()!r}...")
    for match in GETTEXT_RE.finditer(file.read_text("utf-8")):
        msg = match.group("message")
        debug(f"Found {msg!r}")
        messages.add(msg)


#
# make messages nice and formatted
#
pairs: dict[str, str] = {sha1(msg.encode("utf-8")).hexdigest(): msg for msg in messages}  # noqa: S324
template: list[str] = ["sha1,message\n"]

for k, v in sorted(pairs.items()):
    template.append(f"# {v}\n")
    template.append(f'{k},"{v}"\n')


info(f"Writing template to {TEMPLATE_FILE.as_posix()!r}...")
with TEMPLATE_FILE.open("w") as f:
    f.writelines(template)


#
# diff report
#
def remove_values_from_translations(raw: str) -> list[str]:
    """Make every translation neutral and split the text into lines."""
    clean: str = re.sub(r'".+"\n', '"TRANSLATION"\n', raw)
    return clean.splitlines(keepends=True)


report: str = """# diff report for ``{lang}``
```diff
{diff}\
```
"""

differ = Differ()
valueless_template: list[str] = remove_values_from_translations("".join(template))

for file in iter_files(LOCALES_PATH, ".csv"):
    if file.samefile(TEMPLATE_FILE):
        continue

    valueless_translation = remove_values_from_translations(file.read_text("utf-8"))

    info(f"Creating diff for {file.name}...")
    diff = differ.compare(valueless_template, valueless_translation)

    with (report_file := file.with_suffix(".md")).open("w") as f:
        f.write(report.format(lang=file.stem.upper(), diff="".join(diff)))

    debug(f"Wrote diff report into {report_file.as_posix()!r}")
