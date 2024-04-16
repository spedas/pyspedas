"""
Multiplies data by stored spectrogram bins, creates new tplot variable

Notes
-----
Similar to spec_mult.pro in IDL SPEDAS.

"""

import pytplot
import pandas as pd
import copy
import logging

def spec_mult(
        tvar,
        newname=None,
        new_tvar=None
):

    """
    Multiplies the data by the stored spectrogram bins and created a new tplot variable

    Note::
        This analysis routine assumes the data is no more than 2 dimensions.
        If there are more, they may become flattened!

    Parameters:
        tvar : str
            Name of tplot variable
        newname : str
            Name of new tvar in which to store interpolated data.
            Default: If none is specified, a name will be created of the form tvar_specmult.
        new_tvar : str (Deprecated)
            Name of new tvar in which to store interpolated data.  If none is specified, a name will be created.

    Returns:
        None

    Examples:
        >>> pytplot.store_data('h', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]],'v':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> pytplot.spec_mult('h','h_specmult')
        >>> print(pytplot.data_quants['h_specmult'].data)
    """

    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info("spec_mult: The new_tvar parameter is deprecated. Please use newname instead.")
        newname = new_tvar

    if newname is None:
        newname = tvar+'_specmult'
    if 'spec_bins' not in pytplot.data_quants[tvar].coords:
        logging.error("Specified variable must have spec bins stored.  Returning...")
        return
    d, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)
    dataframe = d.values
    specframe = s.values
    new_df = pd.DataFrame(dataframe*specframe, columns=d.columns, index=d.index)
    pytplot.store_data(newname,data={'x': new_df.index,'y': new_df.values})
    pytplot.data_quants[newname].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
    return
