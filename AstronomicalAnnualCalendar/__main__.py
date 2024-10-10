# third party
import click

# local
from .enums import ObservableObjectEnum


def main():  # noqa: D103
    click.secho("Not implemented yet...", err=True, fg="red")
    click.secho(
        f"Debug output: "
        f"\n{ObservableObjectEnum.SUN.internal_id=!r}"
        f"\n{ObservableObjectEnum.SUN.name=!r}"
        f"\n{ObservableObjectEnum.SUN.localized_name=!r}"
        f"\n{ObservableObjectEnum.SUN.is_sun=!r}"
        f"\n{ObservableObjectEnum.SUN.line_color=!r}"
        f"\n{ObservableObjectEnum.SUN.line_strength=!r}",
        fg="green",
    )


if __name__ == "__main__":
    main()
