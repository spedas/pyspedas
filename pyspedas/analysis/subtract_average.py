"""
Subtracts the average (mean) or the median from the data.

Notes
-----
Similar to tsub_average.pro in IDL SPEDAS.

"""
import logging
import pytplot


def subtract_average(names, new_names=None, suffix=None, overwrite=None,
                     median=None):
    """
    Subtracts the average or the median from data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-d'.
    overwrite: bool, optional
        If set, then pytplot variables are replaced.
    median: float, optional
        If it is 0 or not set, then it computes the mean.
        Otherwise, it computes the median.

    Returns
    -------
    None.

    """
    logging.info("subtract_average has been moved to the pytplot.tplot_math package. Please update your imports!")
    logging.info("This version will eventually be removed.")
    pytplot.tplot_math.subtract_average(names=names,new_names=new_names,suffix=suffix,overwrite=overwrite,median=median)
