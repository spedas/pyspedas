import pytplot
import logging

def highlight(variables=None, range=None, color='gray', alpha=0.2, fill=True, edgecolor=None, facecolor=None, hatch=None, delete=False):
    """
    This function highlights a time interval on tplot variables
    """
    if not isinstance(variables, list):
        variables = [variables]
    tvars=pytplot.tplot_wildcard_expand(variables)
    if len(tvars) == 0:
        logging.warning("highlight: No valid tplot names specified")

    for variable in tvars:
        if delete:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'] = None
            continue
        if range is None:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'] = None
            continue
        interval = {'location': range,
                    'color': color,
                    'alpha': alpha,
                    'fill': fill,
                    'edgecolor': edgecolor,
                    'facecolor': facecolor,
                    'hatch': hatch}
        if pytplot.data_quants[variable].attrs['plot_options'].get('highlight_intervals') is None:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'] = [interval]
        else:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'].append(interval)
