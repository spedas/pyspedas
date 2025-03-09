"""
Creates a deep copy of a plot variable, with a new name.

Notes
-----
Allowed wildcards are ? for a single character, * from multiple characters.

"""
import logging
import pytplot
import pyspedas
import copy


def tcopy_one(name_in, name_out):
    """
    Copy a single tplot variable.

    Parameters
    ----------
    name_in : str
        Pytplot name in.
    name_out : str
        Pytplot name out.

    Returns
    -------
    None.

    """
    # Copies one tplot variable
    tvar_old = pytplot.data_quants[name_in]
    tvar_new = copy.deepcopy(tvar_old)
    tvar_new.name = name_out
    pytplot.data_quants.update({name_out: tvar_new})
    logging.info(name_in + ' copied to ' + name_out)


def tcopy(names_in, names_out=None, suffix=None):
    """
    Copy a list of tplot variables.

    Parameters
    ----------
    names_in : str/list of str
        List of pytplot names.
    names_out : str/list of str, optional
        List of pytplot names. The default is None.
    suffix : str, optional
        Suffix to apply to names_in. The default is '-copy'.

    Returns
    -------
    None.

    Examples
    -------
        >>> import pyspedas
        >>> pyspedas.projects.themis.fgm(trange=['2007-03-23','2007-03-24'], probe='a')
        >>> pyspedas.tcopy('tha_fgs_btotal', names_out='thx_fgs_btotal')
        >>> pyspedas.tcopy('tha_fgs_gsm', suffix='_copy')
    """
    names_in = pyspedas.tnames(names_in)
    if len(names_in) < 1:
        logging.error('tcopy: no valid tplot variables found.')
        return

    if suffix is None:
        suffix = '-copy'

    if names_out is None:
        names_out = [s + suffix for s in names_in]

    if isinstance(names_out, str):
        names_out = [names_out]

    if len(names_in) != len(names_out):
        logging.error('tcopy error: List with the names_in does not match list\
              with the names out.')
        return

    for i in range(len(names_in)):
        n = names_in[i]
        o = names_out[i]
        if len(pyspedas.tnames(n)) == 1:
            tcopy_one(n, o)
        else:
            logging.error('tplot name not found: ' + n)
