import logging

import pyspedas
from pyspedas.tplot_tools import tplot_wildcard_expand

logger = logging.getLogger(__name__)


def annotate(
    tvar=None,
    text=None,
    position=None,
    xycoords: str | tuple[str, str] = "axes fraction",
    color=None,
    fontfamily=None,
    fontsize="x-large",
    alpha=1,
    fontvariant="normal",
    fontstyle="normal",
    fontstretch="normal",
    fontweight="normal",
    rotation="horizontal",
    delete=False,
    annotation_clip=None,
):
    """
    Add text annotations to tplot panels.

    Most of the parameters are passed to the matplotlib axes.annotate() method as a dictionary.

    Parameters
    ==========

    tvar: str, int, or list of str or int
        Tplot variable names, zero-based indices, or a list of either
        (wildcards accepted). Non-time-varying variables are skipped with a warning.
    text: str
        Text to add to the plot
    position: tuple or array
        The location for the annotation to appear
    xycoords: str or tuple of str
        The coordinate system to use for the position. 'axes fraction' interprets the positions relative to the panel size. 'data' uses
        data coordinates (times for the x axis, data values for the y axis).  Times should be passed as np.datetime64 objects.
        A tuple selects separate x and y coordinates, for example ('axes fraction', 'data').
    color: str
        Color of the text. Defaults to the global foreground color, or black
        if no foreground color is set.
    fontfamily: str
        Font to be used for the text
    fontsize: str or numeric
        Font size to use.  If numeric, units are in points. (Default: 'x-large')
    alpha: float
        Transparency value to use for the text (default: 1)
    fontvariant: str
        Other attributes of the font to use
    fontstyle: str
        Other attributes of the font to use
    fontstretch: str
        Other attributes of the font to use
    fontweight: str
        Other attributes of the font to use
    rotation:str
        Text orientation ('horizontal', 'vertical')
    delete: bool
        If True, delete all annotations for this variable.
    annotation_clip: bool, optional
        If True, draw the annotation only when its position is inside the axes.
        If False, draw it regardless of position. The default, None, uses
        Matplotlib's behavior: clip only when xycoords is 'data'.

    Notes
    -----
    Each call appends an annotation to the selected variables. With
    ``delete=True``, all annotations on those variables are removed. Call
    ``tplot`` afterwards to draw the updated panels; an existing figure is
    not updated by this function.

    Annotations on a combined variable (pseudovariable) are drawn once after
    its components. Component annotations are also drawn, and are not removed
    by deleting annotations on the combined variable. For combined panels
    with separate left and right y axes, annotations on the combined variable
    use the left axis.

    """

    if not isinstance(tvar, list):
        tvar = [tvar]

    names = tplot_wildcard_expand(tvar)
    if len(names) == 0:
        logger.warning("annotations: no valid tplot variables specified")
        return

    annotations = {
        "text": text,
        "position": position,
        "xycoords": xycoords,
        "fontfamily": fontfamily,
        "fontsize": fontsize,
        "fontvariant": fontvariant,
        "fontstyle": fontstyle,
        "fontstretch": fontstretch,
        "fontweight": fontweight,
        "rotation": rotation,
        "color": color,
        "alpha": alpha,
        "annotation_clip": annotation_clip,
    }

    for name in names:
        if name not in pyspedas.tplot_tools.data_quants:
            logger.info(str(name) + " is currently not in pyspedas.")
            continue

        if isinstance(pyspedas.tplot_tools.data_quants[name], dict):
            logger.warning("Skipping non-time-varying variable %s", name)
            continue

        if delete:
            pyspedas.tplot_tools.data_quants[name].attrs["plot_options"]["extras"]["annotations"] = None
            continue

        if pyspedas.tplot_tools.data_quants[name].attrs["plot_options"]["extras"].get("annotations") is None:
            pyspedas.tplot_tools.data_quants[name].attrs["plot_options"]["extras"]["annotations"] = [annotations]
        else:
            pyspedas.tplot_tools.data_quants[name].attrs["plot_options"]["extras"]["annotations"].append(annotations)
