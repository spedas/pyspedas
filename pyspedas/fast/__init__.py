from .load import load
from pyspedas.utilities.datasets import find_datasets


def dcb(trange=['2001-09-05', '2001-09-06'],
        datatype='', 
        level='k0', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        force_download=False):
    """
    This function loads data from the Fluxgate Magnetometer
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2001-09-05', '2001-09-06']

        datatype: str
            Data type; Unused for dcb
            Default: ''

        level: str
            Data level, valid levels: 'k0', 'l2'
            Default: 'k0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: No suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False, Loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None, all variables are loaded.

        varnames: list of str
            List of variable names to load
            Default: Empty list; all data variables are loaded

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
            Time clip the variables to exactly the range specified in the trange keyword
            Default: False

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False


    Returns
    ----------
        List of str
        List of tplot variables created
        Empty list if no data

    Examples
    --------
    import pyspedas
    from pytplot import tplot
    dcb_vars = pyspedas.fast.dcb(trange=['2001-09-05', '2001-09-06'])
    tplot(['EX','EZ','BX','BY','BZ'])
    """
    return load(instrument='dcb', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)

def acb(trange=['1998-01-05', '1998-01-06'],
        datatype='', 
        level='k0', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        force_download=False):
    """
    This function loads data from the Search-coil Magnetometer
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1998-01-05', '1998-01-06']

        datatype: str
            Data type, Unused for acb data
            Default: ''

        level: str
            Data level, valid levels: 'k0'
            Default: 'k0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: No suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False, Loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  
            Default: None, all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list; all data variables are loaded

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
            Time clip the variables to exactly the range specified in the trange keyword
            Defauly: False

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False

    Returns
    ----------
        List of str
        List of tplot variables created
        Empty list fr no data

    Example
    -------
    import pyspedas
    from pytplot import tplot
    acb_vars = pyspedas.fast.acb()
    tplot('HF_E_SPEC')

    """
    return load(instrument='acb', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)

def esa(trange=['1998-09-05', '1998-09-06'],
        datatype='ies', 
        level='l2', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        force_download=False):
    """
    This function loads data from the Electrostatic Analyzers (ESA)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1998-09-05', '1998-09-06']

        datatype: str
            Data type; Valid options: 'ies' (ion survey data)
                                      'ees' (electron survey data)
                                      'ieb' (ion burst data)
                                      'eeb' (electron burst data)
            Default: 'ies'

        level: str
            Data level, valid levels: 'l2'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: No suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False, Loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None, all variables are loaded.

        varnames: list of str
            List of variable names to load
            Default: Empty list; all data variables are loaded

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
            Time clip the variables to exactly the range specified in the trange keyword
            Default: False

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False

    Returns
    ----------
        List of str
        List of tplot variables created
        Empty list if no data

    Examples
    --------
    import pyspedas
    from pytplot import tplot
    esa_vars = pyspedas.fast.esa()

    """
    return load(instrument='esa', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)

def teams(trange=['1998-09-05', '1998-09-06'],
          datatype='',
          level='k0',
          suffix='',
          get_support_data=False,
          varformat=None,
          varnames=[],
          downloadonly=False,
          notplot=False,
          no_update=False,
          time_clip=False,
          force_download=False):
    """
    This function loads data from the Time-of-flight Energy Angle Mass Spectrograph (TEAMS)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1998-09-05', '1998-09-06']

        datatype: str
            Data type; Unused for TEAMS
            Default: ''

        level:
            Data level: valid levels: 'k0'
            Default: 'k0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: No suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False, Loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None, all variables are loaded.

        varnames: list of str
            List of variable names to load
            Default: Empty list; all data variables are loaded

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
            Time clip the variables to exactly the range specified in the trange keyword
            Default: False

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False

    Returns
    ----------
        List of str
        List of tplot variables created
        Empty list if no data

    Examples
    --------
    import pyspedas
    from pytplot import tplot
    teams_vars = pyspedas.fast.teams(['1998-09-05', '1998-09-06'])
    tplot(['H+', 'H+_low', 'H+_high'])


    """
    return load(instrument='teams', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)


def datasets(instrument=None, label=True):
    return find_datasets(mission='FAST', instrument=instrument, label=label)
