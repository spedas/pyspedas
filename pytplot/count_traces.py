
import numpy as np
import pytplot
import logging

def count_traces(tvar):
    """
    Count the total number of line traces in a variable or list of variables

    Parameter
    ----------
    tvar: str or list of str
        tplot variables with traces to be counted

    Return
    ----------
    int:
        Number of traces found in the input variables.  Spectrograms are not counted.

    Example
    ----------
        >>> import pytplot
        >>> pytplot.store_data('a', data={'x': range(10), 'y': range(10)})
        >>> pytplot.store_data('b', data={'x': range(10), 'y': range(10)})
        >>> pytplot.store_data('pseudovar', data=['a','b'])
        >>> pytplot.count_traces('a')  # 1
        >>> pytplot.count_traces('pseudovar') # 2

    """
    trace_count = 0
    if not isinstance(tvar,list):
        tvar = [tvar]
    for v in tvar:
        if v in pytplot.data_quants.keys():
            data=pytplot.get_data(v, dt=True)

            if pytplot.is_pseudovariable(v):
                components = pytplot.data_quants[v].attrs['plot_options']['overplots_mpl']
                trace_count += count_traces(components)
            else:
                plot_extras = pytplot.data_quants[v].attrs['plot_options']['extras']
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
            logging.warning('The name %s is not in pytplot',v)
    return trace_count
