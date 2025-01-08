from datetime import datetime
from typing import Dict, Optional, Sequence, Union, List

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from pytplot import tplot_options, xlim, tplot_opt_glob
from pytplot.options import options

from .common import plot_init, tplot_with_var_label_panel


def tplot_vl(
        plot_vars: Sequence[any],
        trange: List[str] = ['2017-03-27', '2017-03-28'],
        fig: Optional[Figure] = None,
        font_size: float = 10,
        display=True,
        var_label=[],
        save_png=None,
) -> Figure:
    if fig is None:
        fig = plt.figure()
        # fig = plot_init(xsize=1280, ysize=600, dpi=80, fig=fig)

    var_label_tmp = var_label
    # if 'var_label' in tplot_opt_glob.keys():
    #    var_label_tmp = tplot_opt_glob.get('var_label')
    #    tplot_options('var_label', None)  # Removed temporarily

    # print(plot_vars)
    # print(var_label_tmp)

    # Plot
    fig, axs = tplot_with_var_label_panel(
        tplot_list=plot_vars,
        var_label_list=var_label_tmp,
        fig=fig,
        display=False,
        save_png=save_png,
        return_plot_objects=True,
        font_size=font_size,
    )  # type: ignore

    if display:
        plt.show()

    # xmargin of tplot_options apparently doesn't work, and set it manually with Matplotlib
    ##fig.subplots_adjust(left=0.11, righ=0.87)

    # Restore the original var_label
    # if var_label_tmp != None:
    #    tplot_options('var_label', var_label_tmp)

    return fig






