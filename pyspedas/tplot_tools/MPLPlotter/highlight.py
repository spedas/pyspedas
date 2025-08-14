import pyspedas
from pyspedas.tplot_tools import tplot_wildcard_expand
import logging

def highlight(variables=None, range=None, color='gray', alpha=0.2, fill=True, edgecolor=None, facecolor=None, hatch=None, delete=False):
    """
    Highlight a time interval on tplot variables by adding shading to the plot panel

    Most parameters are passed to the matplotlib axes.axvspan method via a dictionary.

    Parameters
    ==========

    variables: str or list
        tplot variables to add highlights to (Wildcards accepted)
    range: array of floats
        Start and end of highlight time interval, as Unix times
    color: str
        Color to use for the highlight
    alpha: float
        Transparency of highlight
    fill: bool
        Fill color of highlight
    edgecolor: str
        Edge color of highlight
    facecolor: str
        Face color of highlight
    hatch: str
        Hatch pattern to use for highlight
    delete: bool
        If True, delete all highlights associated with the specified variables

    """
    if not isinstance(variables, list):
        variables = [variables]
    tvars=tplot_wildcard_expand(variables)
    if len(tvars) == 0:
        logging.warning("highlight: No valid tplot names specified")

    for variable in tvars:
        if delete:
            pyspedas.tplot_tools.data_quants[variable].attrs['plot_options']['highlight_intervals'] = None
            continue
        if range is None:
            pyspedas.tplot_tools.data_quants[variable].attrs['plot_options']['highlight_intervals'] = None
            continue
        interval = {'location': range,
                    'color': color,
                    'alpha': alpha,
                    'fill': fill,
                    'edgecolor': edgecolor,
                    'facecolor': facecolor,
                    'hatch': hatch}
        if pyspedas.tplot_tools.data_quants[variable].attrs['plot_options'].get('highlight_intervals') is None:
            pyspedas.tplot_tools.data_quants[variable].attrs['plot_options']['highlight_intervals'] = [interval]
        else:
            pyspedas.tplot_tools.data_quants[variable].attrs['plot_options']['highlight_intervals'].append(interval)
