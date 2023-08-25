"""
Smooths a tplot variable.

Uses a boxcar average of the specified width.

Notes
-----
Similar to tsmooth2.pro in IDL SPEDAS.
Also, see: https://www.harrisgeospatial.com/docs/SMOOTH.html

"""
import logging
import pytplot


def smooth(data, width=10, preserve_nans=None):
    """
    Boxcar average.

    Parameters
    ----------
    data : list of floats
        The data should be a one-dim array.
    width : float, optional
        Data window to use for smoothing. The default is 10.
    preserve_nans : bool, optional
        If None, then replace NaNs.

    Returns
    -------
    result : list of floats
        Smoothed data.

    """
    logging.info("smooth has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.tplot_math.smooth(data=data,width=width,preserve_nans=preserve_nans)

def tsmooth(names, width=10, median=None, preserve_nans=None,
            new_names=None, suffix=None, overwrite=None):
    """
    Smooths data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    width: int, optional
        Data window to use for smoothing. The default is 10.
    median: bool, optional
        Apply the median as well.
    preserve_nans: bool, optional
        If None, then replace NaNs.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-s'.
    overwrite: bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None.

    """
    logging.info("tsmooth has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    pytplot.tplot_math.tsmooth(names=names,width=width,median=median,preserve_nans=preserve_nans,new_names=new_names,suffix=suffix,
                               overwrite=overwrite)
