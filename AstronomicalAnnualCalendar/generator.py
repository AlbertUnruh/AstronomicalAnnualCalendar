# standard library
from datetime import UTC, datetime
from pathlib import Path

# third party
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator, HourLocator, MinuteLocator, MonthLocator

# local
from .logger import get_logger
from .models import DataModel, ObservableObjectModel
from .translations import get_text as _


__all__ = ("generate_and_save_graph",)


logger = get_logger("generator@core")


def generate_and_save_graph(
    data: dict[ObservableObjectModel, DataModel], destination: Path, title: str | None = None
) -> None:
    """Generate a graph based on the given data."""
    logger.critical("Data not (correctly) processed yet!")

    dates = [row.date_and_time for row in next(iter(data.values())).rows]
    x_min, x_max, y_min, y_max = 0, 1, min(dates), max(dates)

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    place = next(iter(data.values())).metadata.place
    if title is not None:
        if "%s" in title:
            plt.title(title % place)
        else:
            plt.title(title)
    else:
        plt.title(_("astronomical annual calendar for %s") % place)

    for o, d in data.items():
        if o.is_moon:
            logger.info("Skipping moon!")
            continue

        x, y = [], []
        for row in d.rows:
            if (t := row.culmination_t) is not None:
                x.append(datetime(1970, 1, 1, tzinfo=UTC) + t)
                y.append(row.date_and_time)

        plt.plot_date(x, y, tz=UTC, fmt=".", color=o.line_color.as_hex(), ms=o.line_strength / 8)

    ax = plt.gca()

    ax.xaxis.set_major_formatter(DateFormatter("%H"))
    ax.xaxis.set_major_locator(HourLocator())
    ax.xaxis.set_minor_locator(MinuteLocator(interval=30))

    ax.yaxis.set_major_formatter(DateFormatter("%d.%m"))
    ax.yaxis.set_minor_locator(DayLocator(interval=10))
    ax.yaxis.set_major_locator(MonthLocator(bymonthday=15))

    ax.grid(which="minor", color="#a9a9a9", lw=0.4, ls="--")
    ax.grid(which="major", color="#3b3b3b", lw=0.4, ls="-")

    ax.invert_xaxis()

    plt.savefig(destination)
