
from .subtract_average import subtract_average
import logging


def subtract_median(
        names,
        newname=None,
        new_names=None,
        suffix=None,
        overwrite=None
):
    """
    Subtracts the median from data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    newname: str/list of str, optional
        List of new names for pytplot variables.
        Default: None. If not given, then a suffix is applied.
    new_names: str/list of str, optional (Deprecated)
        List of new names for pytplot variables.
        Default: None. If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply.
        Default: '-d'.
    overwrite: bool, optional
        If set, then pytplot variables are replaced.
        Default: None

    Returns
    -------
    list of str
        Returns a list of new pytplot variables created

    Examples:
        >>> from pytplot import subtract_median

        >>> pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1.,2.,3.,4.,5.]})
        >>> pytplot.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1.,4.,1.,7.,1.,9.,1.]})
        >>> pytplot.tplot_math.subtract_median('a')

    """
    # new_names is deprecated in favor of newname
    if new_names is not None:
        logging.info("subtract_median: The new_names parameter is deprecated. Please use newname instead.")
        newname = new_names

    return subtract_average(names, newname=newname, suffix=suffix, overwrite=overwrite,
                     median=1)
