
from pyspedas.tplot_tools import subtract_average
import logging

def subtract_median(
        names,
        newname=None,
        suffix=None,
        overwrite=None
):
    """
    Subtracts the median from data.

    Parameters
    ----------
    names: str/list of str
        List of pyspedas names.
    newname: str/list of str, optional
        List of new names for tplot variables.
        Default: None. If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply.
        Default: '-d'.
    overwrite: bool, optional
        If set, then tplot variables are replaced.
        Default: None

    Returns
    -------
    list of str
        Returns a list of new tplot variables created

    Examples
    --------
        >>> from pyspedas import subtract_median
        >>> pyspedas.store_data('a', data={'x':[0,4,8,12,16], 'y':[1.,2.,3.,4.,5.]})
        >>> pyspedas.subtract_median('a')

    """

    return subtract_average(names, newname=newname, suffix=suffix, overwrite=overwrite,
                     median=1)
