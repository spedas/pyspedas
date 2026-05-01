import fnmatch
import logging

from pyspedas.tplot_tools import data_quants
from pyspedas.tplot_tools import tplot_names

def wildcard_expand(master_list, patterns, case_sensitive=True, split_whitespace=True, quiet=False):
    """ Find elements in master list matching one or more wild card patterns

    Parameters
    ----------
    master_list: str or list of str
        One or more strings (for example, the set of all tplot variable names)
    patterns: str or list of str
        One or more patterns, which may contain wildcard characters, to be matched agains the master list
    case_sensitive: bool
        A boolean flag indicating whether case-sensitive matching should be performed. Default: True
    split_whitespace: bool
        A boolean flag indicating that master_list or patterns should be treated as space-delimited lists.  Set to False if embedded spaces
        are to be matched.  Default: True
    quiet: bool
        A boolean flag indicating whether to suppress "match not found" warnings. Default: False

    Returns
    -------
    list of str
        A list of elements from master_list that match at least one of the input patterns. Duplicates in the output will be removed.

    Examples
    --------

    >>> from pyspedas import wildcard_expand
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
    if master_list is None:
        logging.warning("wildcard_expand: master_list must be a non-empty string or list")
        return []
    if patterns is None:
        # One could argue that it makes sense to return the entire master list here?
        return []

    matched_items=set()
    ordered_matches=[]

    # Convert inputs to lists if necessary
    if isinstance(patterns, str):
        patterns=[patterns]
    if isinstance(master_list, str):
        master_list=[master_list]

    # Warn if either input is empty
    if len(master_list) == 0 or master_list is None or master_list==['']:
        logging.warning("wildcard_expand: empty master list")
        return []
    if len(patterns) == 0 or patterns is None or patterns==['']:
        logging.warning("wildcard_expand: empty pattern list")
        return []

    # If split_whitespace is true, expand master list and patterns
    if split_whitespace:
        expanded_master_list = []
        for p in master_list:
            p_expanded=p.split(' ')
            expanded_master_list.extend(p_expanded)
        master_list = expanded_master_list
        # Do the same for the patterns
        expanded_patterns=[]
        for pattern in patterns:
            split_pattern=pattern.split(' ')
            expanded_patterns.extend(split_pattern)
        patterns=expanded_patterns


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
        if not found and not quiet:
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


def tplot_wildcard_expand(patterns, case_sensitive=True, quiet=False):
    """ Return tplot variable names matching one or more wildcard patterns

    Parameters
    ----------
    patterns: str, int, list(str!int)
        One or more patterns, which may contain wildcard characters, to be matched against the master list
        Integers are converted to strings using tname_byindex()
    case_sensitive: bool
        A boolean flag indicating whether case-sensitive matching should be performed. Default: True
    quiet: bool
        A boolean flag indicating "no match found" log messages should be suppressed. Default: False

    Returns
    -------
    list of str
        A list of tplot variable names that match at least one of the input patterns. Duplicate values in the output will be removed.

    """
    input_pattern_list = patterns
    if patterns is None:
        return []
    elif isinstance(patterns,str) or isinstance(patterns,int):
        input_pattern_list = [patterns]
    elif isinstance(patterns,list):
        input_pattern_list = patterns
    else:
        logging.warning("tplot_wildcard_expand: patterns must be a string, int or list")
        return []

    string_patterns = []
    # Get list of existing tplot names
    tn = tplot_names(quiet=True)

    if len(tn) == 0:
        if not quiet:
            logging.warning("tplot_wildcard_expand: List of tplot variable names is empty.")
        return []

    # Interpret integers as tplot variable indices
    for item in input_pattern_list:
        if isinstance(item, int):
            name = tname_byindex(item)
            if name is not None:
                string_patterns.append(name)
            else:
                string_patterns.append(item)
        elif isinstance(item,str):
            # tplot names can have embedded spaces, but we also want to allow space-delimited
            # lists. If a space-delimited list is provided, check to see if the un-split version is
            # a valid tplot name.  If not, try splitting it and look for the subpatterns.
            # This case used to also be triggered if there were wildcard characters present.  But this prevented
            # using space-delimited patterns with wildcards.
            if item in tn:
                string_patterns.append(item)
            elif ' ' in item:
                expanded = item.split(' ')
                string_patterns.extend(expanded)
            else:
                # No embedded spaces, and not found in list of names.
                # But there might be wildcards to expand.
                string_patterns.append(item)
        else:
            logging.warning("tplot_wildcard_expand: bad input: "+str(item) +" Patterns must be a string or int")

    return wildcard_expand(tn, patterns=string_patterns, case_sensitive=case_sensitive, split_whitespace=False, quiet=quiet)