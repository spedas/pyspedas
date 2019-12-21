
from .load import load

def emfisis(trange=['2018-11-5', '2018-11-6'], 
        probe='a',
        datatype='magnetometer', 
        level='l3',
        cadence='4sec', # for EMFISIS mag data
        coord='sm', # for EMFISIS mag data
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False):
    """
    This function loads data from the Electric and Magnetic Field Instrument Suite and Integrated Science (EMFISIS) instrument
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """
    return load(instrument='emfisis', trange=trange, probe=probe, datatype=datatype, level=level, cadence=cadence, coord=coord, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)

def rbspice(trange=['2018-11-5', '2018-11-6'], 
        probe='a',
        datatype='tofxeh', 
        level='l3',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False):
    """
    This function loads data from the Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE) instrument
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """
    return load(instrument='rbspice', trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)

def efw(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='', 
        level='l3',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False):
    """
    This function loads data from the Electric Field and Waves Suite (EFW)
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """
    return load(instrument='efw', trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)

def mageis(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='', 
        level='l3',
        rel='rel04',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False):
    """
    This function loads data from the Energetic Particle, Composition, and Thermal Plasma Suite (ECT)
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """
    return load(instrument='mageis', rel=rel, trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)

def hope(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='moments', 
        level='l3',
        rel='rel04',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False):
    """
    This function loads data from the Energetic Particle, Composition, and Thermal Plasma Suite (ECT)
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """
    return load(instrument='hope', rel=rel, trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)

def rept(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='', 
        level='l3',
        rel='rel03',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False):
    """
    This function loads data from the Energetic Particle, Composition, and Thermal Plasma Suite (ECT)
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """
    return load(instrument='rept', rel=rel, trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)

def rps(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='rps-1min', 
        level='l2',
        suffix='',  
        get_support_data=True, 
        varformat=None,
        downloadonly=False):
    """
    This function loads data from the Relativistic Proton Spectrometer (RPS)
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """
    return load(instrument='rps', trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)
