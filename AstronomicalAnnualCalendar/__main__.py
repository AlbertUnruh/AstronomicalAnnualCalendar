# third party
import click

# first party
from AstronomicalAnnualCalendar.enums import ObservableObjectEnum


def main():  # noqa: D103
    click.secho("Not implemented yet...", err=True, fg="red")
    click.secho(
        f"Debug output:"
        f"\n{ObservableObjectEnum.SUN.internal_id=!r}"
        f"\n{ObservableObjectEnum.SUN.name=!r}"
        f"\n{ObservableObjectEnum.SUN.localized_name=!r}"
        f"\n{ObservableObjectEnum.SUN.is_sun=!r}"
        f"\n{ObservableObjectEnum.SUN.line_color=!r}"
        f"\n{ObservableObjectEnum.SUN.line_strength=!r}",
        fg="green",
    )
    # first party
    from AstronomicalAnnualCalendar.regex import (
        DMS_ANGLE_90_REGEX,
        DMS_ANGLE_360_REGEX,
        DMS_COORDINATE_REGEX,
        HMS_ANGLE_REGEX,
        METADATA_REGEX,
    )

    click.secho(
        f"REGEX's:"
        f"\n{HMS_ANGLE_REGEX.pattern=!r}"
        f"\n{DMS_ANGLE_90_REGEX.pattern=!r}"
        f"\n{DMS_ANGLE_360_REGEX.pattern=!r}"
        f"\n{DMS_COORDINATE_REGEX.pattern=!r}"
        f"\n{METADATA_REGEX.pattern=!r}",
        fg="yellow",
    )
    # first party
    from AstronomicalAnnualCalendar.enums import CLIFlags

    click.secho(
        f"Flags:\n{"\n".join(f"{flag!r}" for flag in CLIFlags)}",  # type: ignore
        fg="blue",
    )


if __name__ == "__main__":
    main()
