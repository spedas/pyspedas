# Hacked from esa.py, for esd 3d L2 data files
from pyspedas.projects.themis.load import load


def esd(trange=['2021-03-23', '2021-03-24'],
        probe='c',
        level='l2', #Kept here, but 'l2' is hardcoded in load.py
        datatype = 'peif', #ESD datatypes are in separate files
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads Electrostatic Analyzer 3D  data distribution (ESD) data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2021-03-23', '2021-03-24']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')
            Default: 'c'

        level: str
            Data level; Valid options: 'l2', *** CURRENTLY NOT USED, 'l2' is hardcoded in pyspedas.projects.themis.load
            Default: 'l2'

        datatype: str 
                  'peif', full-mode ion (Default)
                  'peef', full-mode electron
                  'peir', reduced mode ion
                  'peer', reduced mode electron
                  'peib', burst-mode ion
                  'peir', burst-mode electron
            Default: 'peif'

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
        >>> esd_var = pyspedas.projects.themis.esd(probe='a', trange=['2023-11-5', '2023-11-6'], datatype='peer')
        >>> tplot(['eflux', 'data_quality'])

    """
    return load(instrument='esd', trange=trange, level=level, datatype=datatype,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot,
                probe=probe, time_clip=time_clip, no_update=no_update)
