import fnmatch
import logging

from pytplot import data_quants
from .tplot_names import tplot_names

def wildcard_expand(master_list, patterns, case_sensitive=True):
    """ Find elements in master list matching one or more wild card patterns

    Parameters
    ----------
    master_list: str or list of str
        One or more strings (for example, the set of all tplot variable names)
    patterns: str or list of str
        One or more patterns, which may contain wildcard characters, to be matched agains the master list
    case_sensitive: bool
        A boolean flag indicating whether case-sensitive matching should be performed. Default: True

    Returns
    -------
    list of str
        A list of elements from master_list that match at least one of the input patterns. Duplicates in the output will be removed.

    Examples
    --------

    >>> from pytplot import wildcard_expand
    >>> master_list = ['mms1_mec_r_sm', 'mms2_mec_r_sm', 'mms3_mec_r_gsm', 'tha_pos_gsm']
    >>> wildcard_expand(master_list,'*')
    ['mms1_mec_r_sm', 'mms2_mec_r_sm', 'mms3_mec_r_gsm', 'tha_pos_gsm']
    >>> wildcard_expand(master_list, ['mms?_mec_r_sm'])
    ['mms1_mec_r_sm', 'mms2_mec_r_sm']
    >>>wildcard_expand(master_list, ['*SM'], case_sensitive=False)
    ['mms1_mec_r_sm', 'mms2_mec_r_sm', 'mms3_mec_r_gsm', 'tha_pos_gsm']
    >>> wildcard_expand(master_list,'tha_pos_gsm')
    ['tha_pos_gsm']

    """
    if master_list is None or isinstance(master_list, list) is False:
        logging.warning("wildcard_expand: master_list must be a non-empty list")
        return []
    if patterns is None or patterns == '':
        # One could argue that it makes sense to return the entire master list here?
        return []

    matched_items=set()
    ordered_matches=[]

    # Convert inputs to lists if necessary
    if isinstance(patterns, str):
        patterns=[patterns]

    # Warn if either input is empty
    if len(master_list) == 0 or master_list is None:
        logging.warning("wildcard_expand: empty master list")
        return []
    if len(patterns) == 0 or patterns is None:
        logging.warning("wildcard_expand: empty pattern list")
        return []

    # Prepare temporary lists for matching
    if case_sensitive:
        temp_master_list = master_list
        temp_patterns = patterns
    else:
        temp_master_list = [item.lower() for item in master_list]
        temp_patterns = [pattern.lower() for pattern in patterns]

    # Check each pattern against each item in the master list using fnmatchcase
    for pattern in temp_patterns:
        found = False
        for temp_item, original_item in zip(temp_master_list, master_list):
            if fnmatch.fnmatchcase(temp_item, pattern) and original_item not in matched_items:
                found = True
                ordered_matches.append(original_item)
                matched_items.add(original_item)
            elif fnmatch.fnmatchcase(temp_item, pattern):
                found = True
        if not found:
            logging.warning("wildcard_expand: No match found for %s", pattern)

    return ordered_matches

def tname_byindex(tvar_index):
    """ Return a tplot variable name given an integer index

    Parameters
    ----------
    tvar_index: int
        Index into the list of current tplot variable names

    Returns
    -------
    str or None
        Returns the tplot variable name, or None if the index is invalid.

    """
    namelist = list(data_quants.keys())
    if tvar_index >= len(namelist) or tvar_index < 0:
        logging.warning("tname_byindex: index value %d out of bounds", tvar_index)
        return None
    else:
        return namelist[tvar_index]

def tindex_byname(tvar_name):
    """ Return a tplot variable index given a tplot variable name

    Parameters
    ----------
    tvar_name: str
        Name of a tplot variable

    Returns
    -------
    int
        Index of the variable name, or None if not found

    """
    namelist = list(data_quants.keys())
    try:
        index = namelist.index(tvar_name)
        return index
    except ValueError:
        return None


def tplot_wildcard_expand(patterns, case_sensitive=True):
    """ Return tplot variable names matching one or more wildcard patterns

    Parameters
    ----------
    patterns: str, int, list(str!int)
        One or more patterns, which may contain wildcard characters, to be matched against the master list
        Integers are converted to strings using tname_byindex()
    case_sensitive: bool
        A boolean flag indicating whether case-sensitive matching should be performed. Default: True

    Returns
    -------
    list of str
        A list of tplot variable names that match at least one of the input patterns. Duplicate values in the output will be removed.

    """
    input_pattern_list = patterns
    if patterns is None:
        return []
    if isinstance(patterns,str) or isinstance(patterns,int):
        input_pattern_list = [patterns]

    string_patterns = []

    # Interpret integers as tplot variable indices
    for item in input_pattern_list:
        if isinstance(item, int):
            name = tname_byindex(item)
            if name is not None:
                string_patterns.append(name)
            else:
                string_patterns.append(item)
        else:
            string_patterns.append(item)
    tn = tplot_names(quiet=True)
    return wildcard_expand(tn, patterns=string_patterns, case_sensitive=case_sensitive)