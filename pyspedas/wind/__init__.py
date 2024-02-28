from .load import load
from pyspedas.utilities.datasets import find_datasets


def threedp(trange=['1999-11-5', '1999-11-6'],
        datatype='3dp_emfits_e0',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        berkeley=False,
        time_clip=False,
        addmaster=True):
    """
    Load WIND 3DP data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1999-11-5', '1999-11-6']

        datatype: str
            Data type; Valid options: '3dp_ehpd', '3dp_ehsp', '3dp_elm2', '3dp_elpd', '3dp_elsp', '3dp_em', '3dp_emfits_e0',
            '3dp_k0', '3dp_phsp', '3dp_plsp', '3dp_pm', '3dp_sfpd', '3dp_sfsp', '3dp_sopd', '3dp_sosp'
            Default: '3dp_emfits_e0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables will be loaded)

        varnames: list of str
            List of variable names to load (if empty list or not specified,
            all data variables are loaded)
            Default: [] (all variables will be loaded)

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

        addmaster: bool
            If True, use the metadata from a master CDF at SPDF rather than the metadata in the data file
            Default: True

    Returns
    ----------
        List of str
            List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vars = pyspedas.wind.threedp(trange=['1999-11-5', '1999-11-6'],datatype='3dp_emfits_e0')
    >>> tplot(vars)
    """
    return load(instrument='3dp', berkeley=berkeley, addmaster=addmaster, trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def orbit(trange=['1999-11-5', '1999-11-6'],
        datatype='pre_or',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        addmaster=True):
    """
    Load WIND orbit data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1999-11-5', '1999-11-6']

        datatype: str
            Data type; Valid options: 'def_at', 'def_or', 'pre_at', 'pre_or', 'spha_k0'
            Default: 'pre_or'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables will be loaded)

        varnames: list of str
            List of variable names to load (if empty list or not specified,
            all data variables are loaded)
            Default: [] (all variables will be loaded)

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

        addmaster: bool
            If True, use the metadata from a master CDF at SPDF rather than the metadata in the data file
            Default: True


    Returns
    ----------
        List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vars = pyspedas.wind.orbit(trange=['1999-11-5', '1999-11-6'],datatype='pre_or')
    >>> tplot(vars)

    """
    return load(instrument='orbit', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update,addmaster=addmaster)

def sms(trange=['1999-11-5', '1999-11-6'],
        datatype='k0',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        addmaster=True):
    """
    Load data from the WIND Solar Wind and Suprathermal Ion Composition Instrument
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1999-11-5', '1999-11-6']

        datatype: str
            Data type; Valid options: 'k0','l2'
            Default: 'k0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables will be loaded)

        varnames: list of str
            List of variable names to load (if empty list or not specified,
            all data variables are loaded)
            Default: [] (all variables will be loaded)

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

        addmaster: bool
            If True, use the metadata from a master CDF at SPDF rather than the metadata in the data file
            Default: True


    Returns
    ----------
        List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vars = pyspedas.wind.sms(trange=['1999-11-5', '1999-11-6'],datatype='k0')
    >>> tplot(vars)

    """
    return load(instrument='sms', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update,addmaster=addmaster)

def waves(trange=['2018-11-5', '2018-11-6'],
        datatype='h1',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        addmaster=True):
    """
    Load WIND Radio/Plasma Wave (WAVES) data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5','2018-11-6']

        datatype: str
            Data type; Valid options: 'h0', 'h1', 'k0', 'tds'
            Default: 'h1'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables will be loaded)

        varnames: list of str
            List of variable names to load (if empty list or not specified,
            all data variables are loaded)
            Default: [] (all variables will be loaded)

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

        addmaster: bool
            If True, use the metadata from a master CDF at SPDF rather than the metadata in the data file
            Default: True


    Returns
    ----------
        List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vars = pyspedas.wind.waves(trange=['2018-11-5', '2018-11-6'],datatype='h1')
    >>> tplot(vars)

    """
    return load(instrument='waves', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, addmaster=addmaster)

def mfi(trange=['2018-11-5', '2018-11-6'],
        datatype='h0',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        addmaster=True):
    """
    Load data from the WIND Fluxgate Magnetometer
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        datatype: str
            Data type; Valid options: 'h0', 'h1', 'h2', 'h3-rtn', 'h4-rtn', 'k0'
            Default: 'h0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables will be loaded)

        varnames: list of str
            List of variable names to load (if empty list or not specified,
            all data variables are loaded)
            Default: [] (all variables will be loaded)

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

        addmaster: bool
            If True, use the metadata from a master CDF at SPDF rather than the metadata in the data file
            Default: True


    Returns
    ----------
        List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vars = pyspedas.wind.mfi(trange=['2018-11-5', '2018-11-6'],datatype='h0')
    >>> tplot(vars)

    """
    return load(instrument='fgm', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, addmaster=addmaster)

def swe(trange=['2018-11-5', '2018-11-6'],
        datatype='h5',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        addmaster=True):
    """
    Load data from the WIND SWE instrument
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        datatype: str
            Data type; Valid options: 'h0', 'h1', 'h3', 'h4', 'h5', 'k0', 'm0', 'm2'
            Default: 'h5'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables will be loaded)

        varnames: list of str
            List of variable names to load (if empty list or not specified,
            all data variables are loaded)
            Default: [] (all variables will be loaded)

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

        addmaster: bool
            If True, use the metadata from a master CDF at SPDF rather than the metadata in the data file
            Default: True


    Returns
    ----------
        List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vars = pyspedas.wind.swe(trange=['2018-11-5', '2018-11-6'],datatype='h5')
    >>> tplot(vars)

    """
    return load(instrument='swe', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update,addmaster=addmaster)


def datasets(instrument=None, label=True):
    return find_datasets(mission='Wind', instrument=instrument, label=label)
