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
from .monkey import WrapText
from .translations import get_text as _
from .utils import format_to_wh, generate_metadata, get_aac_title, optional_hm_str_to_timedelta


__all__ = ("generate_and_save_explanation", "generate_and_save_graph")


logger = get_logger("generator@core")

_BASE_DATE = datetime(1970, 1, 1, tzinfo=UTC)


def _24h_formatter(x, pos=0) -> str:  # noqa: ANN001, ARG001
    return str(round((num2date(x, UTC) - _BASE_DATE).total_seconds() / (60 * 60)))


def _month_formatter(x, pos=None) -> str:  # noqa: ANN001, ARG001
    return _(num2date(x, UTC).strftime("%B"))


def generate_and_save_graph(
    data: dict[ObservableObjectModel, DataModel],
    destination: Path,
    title: str | None = None,
    size: tuple[float, float] = format_to_wh("A4"),
) -> None:
    """Generate a graph based on the given data."""
    dates = [row.date_and_time for row in next(iter(data.values())).rows]
    x_min, x_max, y_min, y_max = 0, 1, min(dates), max(dates)

    title = get_aac_title(title, next(iter(data.values())).metadata.place)

    fig = plt.figure()

    ax1 = fig.add_subplot()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    major_color, minor_color = "#3b3b3b", "#a9a9a9"

    for ax in (ax1, ax2, ax3):
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.grid(which="minor", color=minor_color, lw=0.4, ls="--")
    ax1.grid(which="major", color=major_color, lw=0.4, ls="-")

    logger.debug(_("detected range from %s to %s") % (y_min.isoformat(" "), y_max.isoformat(" ")))

    ax1.set_title(title, size="x-large", y=1.04)

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
        jumps = np.where(abs(np.diff(x)) > timedelta(0.5))[0] + 1

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

    fig.set_size_inches(size)
    fig.tight_layout(pad=2.4)
    fig.savefig(
        destination,
        dpi=300,
        metadata=generate_metadata(title),
    )


def generate_and_save_explanation(destination: Path, size: tuple[float, float] = format_to_wh("A4")) -> None:
    """Generate a new file with a translated explanation for the astronomical annual calendar."""
    fig = plt.figure(dpi=300, constrained_layout=True)
    ax = fig.add_subplot()
    ax.set_axis_off()

    ax.set_title(2 * "\n" + (title := _("Explanation For The Astronomical Annual Calendar")), size="x-large")

    # is it obvious that this is just a placeholder?
    lorem_ipsum = """\
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore
magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing
elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et
dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat
nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis
dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh
euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.

Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu
feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit
augue duis dolore te feugait nulla facilisi.

Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim
assum. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet
dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit
lobortis nisl ut aliquip ex ea commodo consequat.

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat
nulla facilisis.

At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem
ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut
labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet
clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
sadipscing elitr, At accusam aliquyam diam diam dolore dolores duo eirmod eos erat, et nonumy sed tempor et et invidunt
justo labore Stet clita ea et gubergren, kasd magna no rebum. sanctus sea sed takimata ut vero voluptua. est Lorem ipsum
dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut
labore et dolore magna aliquyam erat.

Consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus
est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet,
consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus.

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore
magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing
elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et
dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat
nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis
dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh
euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.

Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu
feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit
augue duis dolore te feugait nulla facilisi.

xD"""
    left_padding = 0.04
    fig.add_artist(
        WrapText(
            x=left_padding,
            y=0.93,
            text=lorem_ipsum,
            width=1 - 2 * left_padding,
            width_coords=ax.transAxes,
            ha="left",
            va="top",
            clip_on=True,
        )
    )

    fig.set_size_inches(size)
    fig.savefig(
        destination,
        metadata=generate_metadata(title),
    )
