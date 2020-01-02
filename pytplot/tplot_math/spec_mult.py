import pytplot
import pandas as pd
import copy

def spec_mult(tvar,new_tvar=None):
    """
    Multiplies the data by the stored spectrogram bins and created a new tplot variable

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters:
        tvar : str
            Name of tplot variable
        times : int/list
            Desired times for interpolation.
        new_tvar : str
            Name of new tvar in which to store interpolated data.  If none is specified, a name will be created.

    Returns:
        None

    Examples:
        >>> pytplot.store_data('h', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]],'v':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> pytplot.spec_mult('h','h_specmult')
        >>> print(pytplot.data_quants['h_specmult'].data)
    """

    if new_tvar is None:
        new_tvar = tvar+'_specmult'
    if 'spec_bins' not in pytplot.data_quants[tvar].coords:
        print("Specified variable must have spec bins stored.  Returning...")
        return
    d, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)
    dataframe = d.values
    specframe = s.values
    new_df = pd.DataFrame(dataframe*specframe, columns=d.columns, index=d.index)
    pytplot.store_data(new_tvar,data={'x': new_df.index,'y': new_df.values})
    pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
    return
