import pyspedas
from pyspedas.tplot_tools import tplot_wildcard_expand
import logging

def annotate(tvar=None, text=None, position=None,
             xycoords='axes fraction',
             color='black',
             fontfamily=None,
             fontsize='x-large',
             alpha=1,
             fontvariant='normal',
             fontstyle='normal',
             fontstretch='normal',
             fontweight='normal',
             rotation='horizontal',
             delete=False):
    """
    Add text annotatons to tplot panels.

    Most of the parameters are passed to the matplotlib axes.annotate() method as a dictionary.

    Parameters
    ==========

    tvar: str
        A tplot variable name or list of names to add annotations to (wildcards accepted).
    text: str
        Text to add to the plot
    position: tuple or array
        The location for the annotation to appear
    xycoords: str
        The coordinate system to use for the position. 'axes fraction' interprets the positions relative to the panel size. 'data' uses
        data coordinates (times for the x axis, data values for the y axis).  Times should be passed as np.datetime64 objects.
    color: str
        Color of the text (default: 'black')
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

    """

    if isinstance(tvar, int):
        var = list(pyspedas.tplot_tools.data_quants.keys())[tvar]

    if not isinstance(tvar, list):
        tvar = [tvar]

    names = tplot_wildcard_expand(tvar)
    if len(names) == 0:
        logging.warning("annotations: no valid tplot variables specified")
        return

    annotations = {'text': text,
                   'position': position,
                   'xycoords': xycoords,
                   'fontfamily': fontfamily,
                   'fontsize': fontsize,
                   'fontvariant': fontvariant,
                   'fontstyle': fontstyle,
                   'fontstretch': fontstretch,
                   'fontweight': fontweight,
                   'rotation': rotation,
                   'color': color,
                   'alpha': alpha}

    for name in names:

        if name not in pyspedas.tplot_tools.data_quants.keys():
                logging.info(str(name) + " is currently not in pyspedas.")
                continue

        if delete:
            pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras']['annotations'] = None
            continue

        if pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras'].get('annotations') is None:
            pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras']['annotations'] = [annotations]
        else:
            pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras']['annotations'].append(annotations)