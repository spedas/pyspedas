from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

import matplotlib.dates
import numpy as np
import pytplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pytplot import get_data, tplot
from pytplot.MPLPlotter.tplot import get_var_label_ticks
from matplotlib import pyplot as plt

def plot_init(
        xsize: float = 800,
        ysize: float = 1000,
        dpi: int = 100,
        fig: Optional[Figure] = None,
) -> Figure:
    """Initialize plot.

    Need to pass figure initialized by plt.figure() instead of Figure(),
    if you do not use FigureCanvas (GUI)

    Typical value:
        OFA:
            xsize: float = 1280 (px)
            ysize: float = 600 (px)
            dpi: int = 100
        WFC:
            xsize: float = 800 (px)
            ysize: float = 1000 (px)
            dpi: int = 100
    """

    xsize_inch = xsize / dpi
    ysize_inch = ysize / dpi
    if fig is None:
        fig = Figure()
    fig.set_size_inches(xsize_inch, ysize_inch)
    fig.set_facecolor("black")
    return fig


def _preprocess_var_label_panel(
        fig: Figure, variables: Sequence[Any], var_label_list: Sequence[Any]
) -> Tuple[Figure, List[Axes]]:
    # All var labels are plotted as text inside a single subplot (a.k.a panel)
    # So define all panel sizes first
    num_panels = len(variables) + 1
    panel_sizes = [1] * len(variables) + [0.1 * (len(var_label_list) + 2)]
    for var_idx, variable in enumerate(variables):
        if pytplot.data_quants.get(variable) is None:
            continue
        panel_size = (
            pytplot.data_quants[variable]
            .attrs["plot_options"]["extras"]
            .get("panel_size")
        )
        if panel_size is not None:
            panel_sizes[var_idx] = panel_size

    fig.set_facecolor("white")
    gs = fig.add_gridspec(nrows=num_panels, height_ratios=panel_sizes)
    axs = gs.subplots(sharex=True)
    return fig, axs


def _postprocess_var_label_panel(
        variables: Sequence[Any],
        var_label_list: Sequence[Any],
        axs: Sequence[Axes],
        font_size: float,
        save_png=None
) -> None:
    # PyTplot's tplot does not apply xlim if there is no data, so apply here
    x_range = pytplot.tplot_opt_glob.get("x_range")
    if x_range is not None:
        x_range_start = x_range[0]  # type: ignore
        x_range_stop = x_range[1]  # type: ignore

        if isinstance(x_range_start, float):
            if np.isfinite(x_range_start):
                x_range_start = datetime.utcfromtimestamp(x_range_start)
            else:
                x_range_start = datetime.utcfromtimestamp(0)

        if isinstance(x_range_stop, float):
            if np.isfinite(x_range_stop):
                x_range_stop = datetime.utcfromtimestamp(x_range_stop)
            else:
                x_range_stop = datetime.utcfromtimestamp(0)

        x_range = np.array([x_range_start, x_range_stop], dtype="datetime64[ns]")
        for ax in axs:
            ax.set_xlim(x_range)  # type: ignore

    # Postprocess var label panel
    last_data_idx = len(variables) - 1
    last_data_ax = axs[last_data_idx]

    # List[float] (Number of days since epoch)
    xaxis_ticks = last_data_ax.get_xticks().tolist()

    # Get formatted time strings from Matplotlib
    # The format is not identical to IDL version
    # but is suitable for showing in Matplotlib
    # They are the same as xticklabels,
    # but xticklabels is initialized only after figure is drawn
    # So you need to directly use formatter to get the strings
    locator = last_data_ax.xaxis.get_major_locator()
    formatter = matplotlib.dates.ConciseDateFormatter(locator)
    # Ex. 12:34
    time_suffixes = formatter.format_ticks(xaxis_ticks)
    # Ex. 2017-Apr-01
    time_prefix = formatter.get_offset()

    # List[np.datetime64]
    # num2date returns datetime with timezone info (UTC), so make it None
    # to suppress deprecate warning
    xaxis_ticks_dt = [
        np.datetime64(
            matplotlib.dates.num2date(tick_val).replace(tzinfo=None).isoformat(),
            'ns'
        )
        for tick_val in xaxis_ticks
    ]
    xaxis_ticks_dt_str = [
        str(tick_val.astype(str)) for tick_val in xaxis_ticks_dt
    ]

    # Var label panel
    var_label_axis = axs[last_data_idx + 1]
    var_label_axis.spines["top"].set_visible(False)
    var_label_axis.spines["right"].set_visible(False)
    var_label_axis.spines["bottom"].set_visible(False)
    var_label_axis.spines["left"].set_visible(False)
    var_label_axis.tick_params(axis="x", which="both", length=0, labelbottom=False)
    var_label_axis.tick_params(
        axis="y", which="both", length=0, pad=font_size * 3, labelsize=font_size
    )
    var_label_axis.set_ylim(0, len(var_label_list) + 2)

    ys = []
    y_labels = []
    for i in range(len(var_label_list) + 2):
        y = len(var_label_list) + 2 - 0.5 - i
        # print('i, len(var_label_list)+1', i, len(var_label_list)+1)
        # Time prefix (Ex. 2017-Apr-01) is plotted at y = 0.5 (bottom)
        if i == len(var_label_list) + 1:
            y_label = ""
            _, xmax = var_label_axis.get_xlim()
            var_label_axis.text(
                xmax, y, time_prefix, fontsize=font_size, ha="right", va="center"
            )
        else:
            xmin, xmax = var_label_axis.get_xlim()
            # Time suffix (Ex. 12:34) is plotted at y = 1.5 (bottom)
            if i == len(var_label_list):
                y_label = ""
                xaxis_labels = time_suffixes
            # Other var labels are plotted above time suffix
            else:
                label = var_label_list[i]
                # print('label ', label)
                label_data = pytplot.get_data(label, xarray=True, dt=True)
                y_label = label_data.attrs["plot_options"]["yaxis_opt"]["axis_label"]  # type: ignore

                # Switch the type of the time array according to the version of numpy
                if np.__version__ >= "2.0.0":
                    xaxis_labels = get_var_label_ticks(
                        label_data, xaxis_ticks_dt_str
                    )
                else:
                    xaxis_labels = get_var_label_ticks(
                        label_data, xaxis_ticks_dt
                    )
                    # type ignore

            for xaxis_tick, xaxis_label in zip(xaxis_ticks, xaxis_labels):  # type: ignore
                # Sometimes ticks produced by locator can be outside xlim, so let exclude them
                if xmin <= xaxis_tick <= xmax:
                    var_label_axis.text(
                        xaxis_tick,
                        y,
                        xaxis_label,
                        fontsize=font_size,
                        ha="center",
                        va="center",
                    )
            ys.append(y)
            y_labels.append(y_label)
    var_label_axis.set_yticks(ys, y_labels, ha="right")
    if save_png is not None and save_png != '':
        if not save_png.endswith('.png'):
            save_png += '.png'
        plt.savefig(save_png)



def overplot_line(tplot_name: str, ax: Axes) -> None:
    """Substitute overplot in IDL because PyTplot has not yet implemented it"""
    data = get_data(tplot_name, dt=True)
    if data is None:
        return

    metadata = get_data(tplot_name, metadata=True)
    line_opts: Dict[Any] = metadata["plot_options"]["line_opt"]  # type: ignore
    plot_extras: Dict[Any] = metadata["plot_options"]["extras"]  # type: ignore

    line_color: Optional[List[Any]] = plot_extras.get("line_color")
    if line_color is not None:
        color = line_color[0]
    else:
        color = None

    line_width: Optional[List[float]] = line_opts.get("line_width")
    if line_width is not None:
        width = line_width[0]
    else:
        width = 0.5

    line_style_user: Optional[List[str]] = line_opts.get("line_style_name")
    if line_style_user is not None:
        line_style = []
        for linestyle in line_style_user:
            if linestyle == "solid_line":
                line_style.append("solid")
            elif linestyle == "dot":
                line_style.append("dotted")
            elif linestyle == "dash":
                line_style.append("dashed")
            elif linestyle == "dash_dot":
                line_style.append("dashdot")
            else:
                line_style.append(linestyle)
    else:
        line_style = ["solid"]
    line_style = line_style[0]

    ax.plot(
        data.times,
        data.y,
        color=color,
        linewidth=width,
        linestyle=line_style,
    )


def tplot_with_var_label_panel(
        tplot_list: Sequence[str],
        var_label_list: Sequence[str],
        fig: Figure,
        display: bool = False,
        save_png=None,
        return_plot_objects: bool = True,
        font_size: float = 10,
):
    # Enhanced tplot changing var label from axis to panel
    # Preprocess var panels
    fig, axs = _preprocess_var_label_panel(fig, tplot_list, var_label_list)

    # Then tplot
    fig, axs = tplot(
        tplot_list,
        return_plot_objects=return_plot_objects,
        fig=fig,
        axis=axs,
        display=display,
        save_png=None,
    )
    # Postprocess var panels
    _postprocess_var_label_panel(tplot_list, var_label_list, axs, font_size, save_png=save_png)

    if return_plot_objects:
        return fig, axs