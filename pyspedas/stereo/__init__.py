
from .load import load


def het(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        level='l1',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the High Energy Telescope

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'
        
        level: str
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> sit_vars = pyspedas.stereo.het(trange=['2013-1-5', '2013-1-6'])
        >>> tplot(sit_vars)

    """

    return load(instrument='het', trange=trange, probe=probe, suffix=suffix, level=level,
                get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                notplot=notplot, time_clip=time_clip, no_update=no_update)


def let(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        level='l1',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Low Energy Telescope

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        level: str
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted. 
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> sit_vars = pyspedas.stereo.let(trange=['2013-1-5', '2013-1-6'])
        >>> tplot(sit_vars)

    """

    return load(instrument='let', trange=trange, probe=probe, suffix=suffix, level=level,
                get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                notplot=notplot, time_clip=time_clip, no_update=no_update)


def sit(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        level='l1',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Suprathermal Ion Telescope

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        level: str
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> sit_vars = pyspedas.stereo.sit(trange=['2013-1-5', '2013-1-6'])
        >>> tplot(sit_vars)

    """

    return load(instrument='sit', trange=trange, probe=probe, suffix=suffix, level=level,
                get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                notplot=notplot, time_clip=time_clip, no_update=no_update)


def sept(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        level='l1',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Solar Electron Proton Telescope

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        level: str
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> sept_vars = pyspedas.stereo.sept(trange=['2013-1-5', '2013-1-6'])
        >>> tplot(sit_vars)

    """

    return load(instrument='sept', trange=trange, probe=probe, suffix=suffix, level=level,
                get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                notplot=notplot, time_clip=time_clip, no_update=no_update)


def ste(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        level='l1',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Suprathermal Electron Telescope

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        level: str
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    """

    return load(instrument='ste', trange=trange, probe=probe, suffix=suffix, level=level,
                get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                notplot=notplot, time_clip=time_clip, no_update=no_update)


def swea(trange=['2013-1-5', '2013-1-6'],
        probe='a',
        datatype='spec',
        level='l1',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Solar Wind Electron Analyzer

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        datatype: str
            Data type; Valid options: disb, dist, spec
            Default: 'spec'

        level: str
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> swea_vars = pyspedas.stereo.swea(trange=['2013-1-5', '2013-1-6'])
        >>> tplot(sit_vars)

    """
    return load(instrument='swea', trange=trange, probe=probe, datatype=datatype, suffix=suffix, level=level,
                get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                notplot=notplot, time_clip=time_clip, no_update=no_update)


def mag(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        datatype='8hz',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the magnetometer
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        datatype: str
            Data type; Valid options: 8hz, 32hz
            Default: '8hz'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> mag_vars = pyspedas.stereo.mag(trange=['2013-1-5', '2013-1-6'])
        >>> tplot('BFIELD')

    """
    return load(instrument='mag', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def plastic(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        datatype='1min',
        level='l2',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the PLASTIC instrument
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        datatype: str
            Data type; Valid options: 1min
            Default: '1min'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> plastic_vars = pyspedas.stereo.plastic(trange=['2013-11-5', '2013-11-6'])
        >>> tplot(['proton_number_density', 'proton_bulk_speed', 'proton_temperature', 'proton_thermal_speed'])

    """
    return load(instrument='plastic', trange=trange, probe=probe, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def waves(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        datatype='hfr',
        level='l3',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the WAVES instrument
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        datatype: str
            Data type; Valid options: hfr, lfr
            Default: 'hfr'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> hfr_vars = pyspedas.stereo.waves(trange=['2013-11-5', '2013-11-6'])
        >>> tplot(['PSD_FLUX'])

    """
    return load(instrument='waves', trange=trange, probe=probe, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def beacon(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the WAVES instrument
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        suffix: str
            The tplot variable names will be given this suffix. 
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in. 

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspdedas
        >>> from pytplot import tplot
        >>> beacon_vars = pyspedas.stereo.beacon(trange=['2013-11-5', '2013-11-6'])
        >>> tplot(['MAGBField'])

    """
    return load(instrument='beacon', trange=trange, probe=probe, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)
