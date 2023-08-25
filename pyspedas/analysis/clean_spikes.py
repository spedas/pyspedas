"""
Creates a new tplot variable that has spikes removed.

Notes
-----
Similar to clean_spikes.pro in IDL SPEDAS.

"""
import logging
import pytplot


def clean_spikes(names, nsmooth=10, thresh=0.3, sub_avg=False,
                 new_names=None, suffix=None, overwrite=None):
    """
    Clean spikes from data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-avg'.
    overwrite: bool, optional
        Replace the existing tplot name.
    nsmooth: int, optional
        the number of data points for smoothing
    thresh: float, optional
        threshold value
    sub_avg: bool, optional
        if set, subtract the average value of the data
        prior to checking for spikes

    Returns
    -------
    None.

    """
    logging.info("clean_spikes has been moved to the pytplot.tplot_math package. Please update your imports!")
    logging.info("This version will eventually be removed.")
    pytplot.tplot_math.clean_spikes(names=names, nsmooth=nsmooth, thresh=thresh, sub_avg=sub_avg, new_names=new_names,
                                    suffix=suffix,overwrite=overwrite)
