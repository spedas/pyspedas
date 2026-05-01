"""
Multiplies data by stored spectrogram bins, creates new tplot variable

Notes
-----
Similar to spec_mult.pro in IDL SPEDAS.

"""

import pyspedas
from pyspedas.tplot_tools import store_data, convert_tplotxarray_to_pandas_dataframe
import pandas as pd
import copy
import logging

def spec_mult(
        tvar,
        newname=None,
):

    """
    Multiplies the data by the stored spectrogram bins and created a new tplot variable

    Note::
        This analysis routine assumes the data is no more than 2 dimensions.
        If there are more, they may become flattened!

    Parameters
    ----------
        tvar : str
            Name of tplot variable
        newname : str
            Name of new tvar in which to store interpolated data.
            Default: If none is specified, a name will be created of the form tvar_specmult.

    Returns
    -------
        None

    Examples
    --------
        >>> pyspedas.store_data('h', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]],'v':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> pyspedas.spec_mult('h')

    """

    if newname is None:
        newname = tvar+'_specmult'
    if 'spec_bins' not in pyspedas.tplot_tools.data_quants[tvar].coords:
        logging.error("Specified variable must have spec bins stored.  Returning...")
        return
    d, s = convert_tplotxarray_to_pandas_dataframe(tvar)
    dataframe = d.values
    specframe = s.values
    new_df = pd.DataFrame(dataframe*specframe, columns=d.columns, index=d.index)
    store_data(newname,data={'x': new_df.index,'y': new_df.values})
    pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)
    return
