[![GitHub License](https://img.shields.io/github/license/AlbertUnruh/AstronomicalAnnualCalendar)](https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/blob/develop/LICENSE)
[![Python version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FAlbertUnruh%2FAstronomicalAnnualCalendar%2Frefs%2Fheads%2Fdevelop%2Fpyproject.toml&query=%24.tool.poetry.dependencies.python&label=Python)](https://python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</br>
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/AlbertUnruh/AstronomicalAnnualCalendar/develop.svg)](https://results.pre-commit.ci/latest/github/AlbertUnruh/AstronomicalAnnualCalendar/develop)
[![Code QL](https://img.shields.io/github/actions/workflow/status/AlbertUnruh/AstronomicalAnnualCalendar/.github%2Fworkflows%2Fcodeql.yml?branch=develop&logo=github&label=CodeQL)](https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/actions/workflows/codeql.yml)
[![pytest](https://img.shields.io/github/actions/workflow/status/AlbertUnruh/AstronomicalAnnualCalendar/.github%2Fworkflows%2Fpytest.yml?branch=develop&logo=github&label=pytest)](https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/actions/workflows/pytest.yml)
</br>
[![GitHub Issues](https://img.shields.io/github/issues-raw/AlbertUnruh/AstronomicalAnnualCalendar)](https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/issues)
[![GitHub PRs](https://img.shields.io/github/issues-pr-raw/AlbertUnruh/AstronomicalAnnualCalendar)](https://github.com/AlbertUnruh/AstronomicalAnnualCalendar/pulls)

# AstronomicalAnnualCalendar

<!-- EN -->
🇬🇧 A tool to help to generate the astronomical annual calendar
</br>→ see [README-en.md](./README-en.md "English version")


<!-- DE -->
🇩🇪 Ein Werkzeug um den astronomischen Jahreskalender zu generieren
</br>→ siehe [README-de.md](./README-de.md "Deutsche Version")


### You want to feed your own data to the program?

Then have a look at the specifications over at ``python AstronomicalAnnualCalendar specification``!

The command will give you an overview over the currently implemented parsers
*(even though they may not technically parse...)*
which allows you to view the specific specification for any selected parser.

All parsers have to respect the annotations given by the ABC. Otherwise, it will lead to unexpected runtime errors!
