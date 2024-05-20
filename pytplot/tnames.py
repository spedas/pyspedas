"""
Find all pytplot names that follow a pattern that may contain a wildcard.

Notes
-----
Allowed wildcards are ? for a single character, * from multiple characters.

"""
import fnmatch
from pytplot import tplot_names


def tnames(pattern=None):
    """
    Find pytplot names matching a wildcard pattern.

    Parameters
    ----------
    pattern : str, optional
        Patern to search for. The default is None, which returns all names.

    Returns
    -------
    name_list : list of str
        List of pytplot variables.

    Examples
    -------
        >>> import pytplot
        >>> from pyspedas.themis import fgm 
        >>> fgm(trange=['2007-03-23','2007-03-24'], probe='a')
        >>> pytplot.tnames('tha_fgs*')
        >>> pytplot.tnames('th?_fgs_gsm')
    """
    name_list = list()
    all_names = tplot_names(quiet=True)

    if pattern is None:
        name_list.extend(all_names)
    else:
        if isinstance(pattern, str):
            name_list.extend(fnmatch.filter(all_names, pattern))
        else:
            for p in pattern:
                name_list.extend(fnmatch.filter(all_names, p))

    return name_list
