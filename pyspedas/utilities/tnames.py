"""
Find all pytplot names that follow a pattern that may contain a wildcard.

Notes
-----
Allowed wildcards are ? for a single character, * from multiple characters.

"""
import logging
import pytplot

def tnames(pattern=None):
    """
    Find pytplot names.

    Parameters
    ----------
    pattern : str, optional
        Patern to search for. The default is None, which returns all names.

    Returns
    -------
    name_list : list of str
        List of pytplot variables.

    """
    logging.info("tnames has been moved to the pytplot package. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.tnames(pattern)
