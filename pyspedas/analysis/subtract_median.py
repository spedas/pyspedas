"""
Subtracts the median from the data.

Notes
-----
Similar to tsub_average.pro in IDL SPEDAS.

"""
from .subtract_average import subtract_average


def subtract_median(names, new_names=None, suffix=None, overwrite=None):
    """
    Subtracts the median from data.

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

    Returns
    -------
    None.

    """
    subtract_average(names, new_names=None, suffix=None, overwrite=None,
                     median=1)
