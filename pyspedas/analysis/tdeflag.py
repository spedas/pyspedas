"""
Removes NaNs and other flags.

Notes
----
Allowed wildcards are ? for a single character, * from multiple characters.
Similar to tdeflag.pro in IDL SPEDAS.
Moved to PyTplot/pytplot/tplot_math, 2023-11-30
"""
import logging
import pyspedas
import pytplot
import numpy

# Added default method="remove_nan" (inadvertently committed under a different log message)

def tdeflag(names, method="remove_nan", new_names=None, suffix=None,
            overwrite=None):
    """
    Remove NaNs from tplot variables.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    method: str, optional
        Method to apply. Default is 'remove_nan.
        Other options 'repeat' (repeat last good value).
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-deflag'.
    overwrite: bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None.

    """
    logging.info("tdeflag has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    pytplot.tplot_math.tdeflag(names,method=method,new_names=new_names,
                               suffix=suffix,overwrite=overwrite)
