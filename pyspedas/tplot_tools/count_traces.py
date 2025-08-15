
import numpy as np
import pyspedas
from pyspedas.tplot_tools import get_data, is_pseudovariable
import logging

def count_traces(tvar):
    """
    Count the total number of line traces in a variable or list of variables

    Parameters
    ----------
    tvar: str or list of str
        tplot variables with traces to be counted

    Returns
    -------
    int
        Number of traces found in the input variables.  Spectrograms are not counted.

    Examples
    --------
        >>> import pyspedas
        >>> pyspedas.store_data('a', data={'x': range(10), 'y': range(10)})
        >>> pyspedas.store_data('b', data={'x': range(10), 'y': range(10)})
        >>> pyspedas.store_data('pseudovar', data=['a','b'])
        >>> pyspedas.count_traces('a')  # 1
        >>> pyspedas.count_traces('pseudovar') # 2

    """
    trace_count = 0
    if not isinstance(tvar,list):
        tvar = [tvar]
    for v in tvar:
        if v in pyspedas.tplot_tools.data_quants.keys():
            data=get_data(v, dt=True)

            if is_pseudovariable(v):
                components = pyspedas.tplot_tools.data_quants[v].attrs['plot_options']['overplots_mpl']
                trace_count += count_traces(components)
            else:
                plot_extras = pyspedas.tplot_tools.data_quants[v].attrs['plot_options']['extras']
                if plot_extras.get('spec') is not None:
                    spec = plot_extras['spec']
                else:
                    spec = False

                if len(data.y.shape) == 1:
                    num_lines = 1
                else:
                    num_lines = data.y.shape[1]

                if not spec:
                    trace_count += num_lines
        else:
            logging.warning('The name %s is not in pyspedas',v)
    return trace_count
