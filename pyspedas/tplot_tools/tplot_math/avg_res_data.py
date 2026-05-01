import pyspedas
import numpy as np
import copy
import logging

def avg_res_data(tvar,res,newname=None):
    """
    Averages the variable over a specified period of time.

    Parameters
    ----------
        tvar : str
            Name of tplot variable.
        res : int/float
            The new data resolution
        newname : str
            Name of new tvar for averaged data.  If not set, then the data in tvar is replaced.

    Returns
    -------
        None

    Note
    ----

    This routine uses the xarray coarsen() method to reduce the time resolution.  It will only work if the
    data is evenly gridded, and the res parameter evenly divides the number of samples.
    For most purposes, it is more appropriate to use pyspedas.avg_data() instead.

    Examples
    --------

        >>> #Average the data over every two seconds
        >>> pyspedas.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> pyspedas.avg_res_data('d',2,'d2res')

    """

    tvar_new = pyspedas.tplot_tools.data_quants[tvar].coarsen(time=res, boundary='trim').mean()
    tvar_new.name = pyspedas.tplot_tools.data_quants[tvar].name
    tvar_new.attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)

    if newname is None:
        pyspedas.tplot_tools.data_quants[tvar] = newname
    else:
        if 'spec_bins' in pyspedas.tplot_tools.data_quants[tvar].coords:
           pyspedas.store_data(newname, data={'x': tvar_new.coords['time'].values, 'y': tvar_new.values,
                                               'v': tvar_new.coords['spec_bins'].values})
        else:
           pyspedas.store_data(newname, data={'x': tvar_new.coords['time'].values, 'y': tvar_new.values})

        pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)

    return

