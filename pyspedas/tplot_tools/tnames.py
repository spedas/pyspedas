import re
import logging
from pyspedas.tplot_tools import tplot_names, tplot_wildcard_expand


def tnames(pattern=None, regex=None):
    """
    Find tplot names matching a wildcard pattern.

    Parameters
    ----------
    pattern : str or list of str, optional
        Pattern(s) to search for.
        It can be a string or a list of strings (multiple patterns).
        Each pattern can contain wildcards such as * and ?, using unix-style matching.
        The default is None
    regex : str, optional
        Regular expression pattern to search for.
        If regex is provided, the pattern argument is ignored.
        The default is None.
        If both pattern and regex are None, all tplot names are returned.

    Returns
    -------
    name_list : list of str
        List of tplot variables.

    Examples
    -------
        >>> import pyspedas
        >>> import pyspedas
        >>> from pyspedas.projects.themis import fgm
        >>> fgm(trange=['2007-03-23','2007-03-24'], probe='a')
        >>> pyspedas.tnames('tha_fgs*')
        >>> pyspedas.tnames('th?_fgs_gsm')
    """
    name_list = list()
    all_names = tplot_names(quiet=True)

    if len(all_names) < 1:
        # No tplot variables found
        pass
    elif pattern is None and regex is None:
        name_list.extend(all_names)
    elif regex is not None:
        # Use re to find all names that match the regular expression
        try:
            # Check if regex is a valid regular expression
            re.compile(regex)

            for p in all_names:
                if re.match(regex, p):
                    name_list.append(p)
        except re.error:
            logging.error("Invalid regular expression.")
    elif pattern is not None:
        # Switch to tplot_wildcard_expand for improved handling of tplot names with embedded spaces
        name_list = tplot_wildcard_expand(pattern)

    return name_list
