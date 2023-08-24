"""
Time clip of data.

Notes
-----
Similar to tclip.pro in IDL SPEDAS.

"""
import logging
import pytplot


def time_clip(names, time_start, time_end, new_names=None, suffix=None,
              overwrite=None):
    """
    Clip data from time_start to time_end.

    Parameters:
    names: str/list of str
        List of pytplot names.
    time_start : float
        Start time.
    time_end : float
        End time.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-m'.
    overwrite: bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None.

    """
    logging.info("time_clip has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    pytplot.tplot_math.time_clip(names=names,time_start=time_start,time_end=time_end,new_names=new_names,suffix=suffix,
                                 overwrite=overwrite)