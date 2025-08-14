from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

import matplotlib.dates
import numpy as np
import pyspedas
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pyspedas.tplot_tools import get_data
from pyspedas.tplot_tools import get_var_label_ticks
from matplotlib import pyplot as plt

def var_label_panel(
        variables: Sequence[Any],
        var_label_list: Sequence[Any],
        axs: Sequence[Axes],
        font_size: float
) -> None:

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
                label_data = get_data(label, xarray=True, dt=True)
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

