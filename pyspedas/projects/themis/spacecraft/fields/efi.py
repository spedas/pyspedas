
import logging
from pyspedas import wildcard_expand
from pyspedas.projects.themis.load import load


def efi(trange=['2007-03-23', '2007-03-24'],
        probe='c',
        level='l2',
        datatype=None,
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads Electric Field Instrument (EFI) data

    Parameters
    ----------

        trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')
            Default: 'c'

        level: str
            Processing level; Valid options: 'l1', 'l2'
            Default: 'l2'

        datatype: str or list of str
            Data type; Valid L1 options::

                'eff', Fast survey E12, E34, E56 waveforms
                'efp', Particle burst E12, E34, E56 waveforms
                'efw', Wave burst E12 E34, E56 waveforms
                'vaf', Fast survey voltage group A, V1-V6 boom voltages
                'vap', Particle burst voltage group A, V1-V6 boom voltages
                'vaw', Wave burst voltage group A, V1-V6 boom voltages
                'vbf', Fast survey voltage group B, V1-V6 boom voltages
                'vbp', Particle burst voltage group B, V1-V6 boom voltages
                'vbw', Wave burst voltage group B, V1-V6 boom voltages
                L1 default: [eff. efp, efw, vaf. vap, vaw]

            Valid L2 options::

                'efi', Fast survey E field vectors and other quantities
                'efp', Particle burst E field vectors
                'efw', Wave burst E field vectors
                L2 default: efi

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  
            Default: False; only loads data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None; all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list, so all data variables are loaded

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified
            in the trange keyword
            Default: False

    Returns
    -------
    List of str
        List of tplot variables created
        Empty list if no data
    
    Example
    -------
        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> efi_vars = pyspedas.projects.themis.efi(probe='d', trange=['2013-11-5', '2013-11-6'])
        >>> tplot('thd_efs_dot0_gse')


    """
    valid_levels = ['l1', 'l2']
    valid_l1_datatypes = ['eff', 'efp', 'efw', 'vaf', 'vap', 'vaw', 'vbf', 'vbp', 'vbw']
    default_l1_datatypes = ['eff', 'efp', 'efw', 'vaf', 'vap', 'vaw']  # omit vb* by default
    valid_l2_datatypes = ['efi', 'efp', 'efw']
    default_l2_datatypes = ['efi'] # omit efp and efw unless specifically requested

    if level.lower() not in valid_levels:
        logging.error("Unrecognized level %s", level)
        return []

    level=level.lower()

    if level == 'l1':
        valid_datatypes=valid_l1_datatypes
        default_datatypes=default_l1_datatypes
    else:
        valid_datatypes=valid_l2_datatypes
        default_datatypes=default_l2_datatypes

    if datatype is None:
        selected_datatype=default_datatypes
    else:
        selected_datatype=wildcard_expand(valid_datatypes, datatype, case_sensitive=False)

    if len(selected_datatype) == 0:
        logging.error("No valid datatypes selected")
        return []

    return load(instrument='efi', trange=trange, level=level,
                datatype=selected_datatype,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot,
                probe=probe, time_clip=time_clip, no_update=no_update)
