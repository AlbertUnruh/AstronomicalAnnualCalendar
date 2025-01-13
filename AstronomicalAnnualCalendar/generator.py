# standard library
from datetime import UTC, datetime, timedelta
from itertools import chain
from pathlib import Path

# third party
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import HourLocator, MinuteLocator, MonthLocator, num2date
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, NullFormatter

# local
from .logger import get_logger
from .models import DataModel, ObservableObjectModel
from .translations import get_text as _
from .utils import generate_metadata, get_aac_title, optional_hm_str_to_timedelta


__all__ = ("generate_and_save_graph",)


logger = get_logger("generator@core")

_BASE_DATE = datetime(1970, 1, 1, tzinfo=UTC)


def _24h_formatter(x, pos=0) -> str:  # noqa: ANN001, ARG001
    return str(round((num2date(x, UTC) - _BASE_DATE).total_seconds() / (60 * 60)))


def _month_formatter(x, pos=None) -> str:  # noqa: ANN001, ARG001
    return _(num2date(x, UTC).strftime("%B"))


def generate_and_save_graph(
    data: dict[ObservableObjectModel, DataModel], destination: Path, title: str | None = None
) -> None:
    """Generate a graph based on the given data."""
    dates = [row.date_and_time for row in next(iter(data.values())).rows]
    x_min, x_max, y_min, y_max = 0, 1, min(dates), max(dates)

    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    major_color, minor_color = "#3b3b3b", "#a9a9a9"

    for ax in (ax1, ax2, ax3):
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.grid(which="minor", color=minor_color, lw=0.4, ls="--")
    ax1.grid(which="major", color=major_color, lw=0.4, ls="-")

    logger.debug(_("detected range from %s to %s") % (y_min.isoformat(" "), y_max.isoformat(" ")))

    plt.title(title := get_aac_title(title, next(iter(data.values())).metadata.place))

    legend: list[Line2D] = []
    for o, d in data.items():
        if o.is_moon:
            logger.info(_("Skipping %s!") % o.name)
            continue

        x, y = [], []
        for row in d.rows:
            if (t := optional_hm_str_to_timedelta(row.culmination)) is not None:
                x.append(_BASE_DATE + t)
                y.append(row.date_and_time)

        # where the object jumps from 24 to 0 (and would jump across the whole plot to connect to next point)
        jumps = np.where(np.diff(x) > timedelta(0.5))[0] + 1

        for x_, y_ in zip(np.split(x, jumps), np.split(y, jumps), strict=False):
            ax1.plot(x_, y_, "-", color=o.line_color.as_hex(), lw=o.line_strength / 2)

        legend.append(Line2D([], [], color=o.line_color.as_hex(), lw=o.line_strength**0.5, label=o.name))

    ax1.legend(handles=legend)

    # major formatter
    ax1.xaxis.set_major_formatter(FuncFormatter(_24h_formatter))
    # major locator
    ax1.xaxis.set_major_locator(HourLocator())
    # minor locator
    ax1.xaxis.set_minor_locator(MinuteLocator(interval=30))

    # major formatter
    ax1.yaxis.set_major_formatter(NullFormatter())
    ax2.yaxis.set_major_formatter(_month_formatter)
    ax3.yaxis.set_major_formatter(NullFormatter())
    # major locator
    ax1.yaxis.set_major_locator(MonthLocator(bymonthday=1))  # month border
    ax2.yaxis.set_major_locator(MonthLocator(bymonthday=16))  # place label approximately in the middle of each month
    # minor locator
    ax2.yaxis.set_minor_locator(MonthLocator(bymonthday=11))  # 1st 10-day marker
    ax3.yaxis.set_minor_locator(MonthLocator(bymonthday=21))  # 2nd 10-day marker

    for tick in chain(
        ax1.xaxis.get_minor_ticks(),
        ax1.yaxis.get_major_ticks(),
        ax1.yaxis.get_minor_ticks(),
        ax2.yaxis.get_major_ticks(),
        ax2.yaxis.get_minor_ticks(),
        ax3.yaxis.get_major_ticks(),
        ax3.yaxis.get_minor_ticks(),
    ):
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)

    ax1.tick_params(top=True, labeltop=True, bottom=True, labelbottom=True)
    ax1.invert_xaxis()

    ax1.set_zorder(max(a.get_zorder() for a in (ax2, ax3)) + 1)  # move ax1 to foreground
    for ax in (ax1, ax2, ax3):
        ax.patch.set_visible(False)  # make background transparent

    plt.gcf().set_size_inches(8.27, 11.69)  # A4 (vertical/portrait)
    plt.savefig(
        destination,
        dpi=300,
        metadata=generate_metadata(title),
    )
