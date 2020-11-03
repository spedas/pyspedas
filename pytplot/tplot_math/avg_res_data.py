import pytplot
import numpy as np
import copy

def avg_res_data(tvar,res,new_tvar=None):
    """
    Averages the variable over a specified period of time.

    Parameters:
        tvar1 : str
            Name of tplot variable.
        res : int/float
            The new data resolution
        new_tvar : str
            Name of new tvar for averaged data.  If not set, then the data in tvar is replaced.

    Returns:
        None

    Examples:
        >>> #Average the data over every two seconds
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> pytplot.avg_res_data('d',2,'d2res')
        >>> print(pytplot.data_quants['d'].values)
    """

    tvar_new = pytplot.data_quants[tvar].coarsen(time=res, boundary='trim').mean()
    tvar_new.name = pytplot.data_quants[tvar].name
    tvar_new.attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    if new_tvar is None:
        pytplot.data_quants[tvar] = tvar_new
    else:
        if 'spec_bins' in pytplot.data_quants[tvar].coords:
            pytplot.store_data(new_tvar, data={'x': tvar_new.coords['time'].values, 'y': tvar_new.values,
                                               'v': tvar_new.coords['spec_bins'].values})
        else:
            pytplot.store_data(new_tvar, data={'x': tvar_new.coords['time'].values, 'y': tvar_new.values})

        pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    return

