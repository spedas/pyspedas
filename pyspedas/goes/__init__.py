
from .load import load

def fgm(trange=['2013-11-5', '2013-11-6'], 
        probe='15',
        datatype='1min', 
        suffix='',  
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GOES Magnetometer
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='fgm', trange=trange, probe=probe, datatype=datatype, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def eps(trange=['2013-11-5', '2013-11-6'], 
        probe='12',
        datatype='1min', 
        suffix='',  
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GOES energetic particle sensor
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='eps', trange=trange, probe=probe, datatype=datatype, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def epead(trange=['2013-11-5', '2013-11-6'], 
        probe='15',
        datatype='1min', 
        suffix='',  
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GOES Electron, Proton, Alpha Detector
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='epead', trange=trange, probe=probe, datatype=datatype, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def maged(trange=['2013-11-5', '2013-11-6'], 
        probe='15',
        datatype='1min', 
        suffix='',  
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GOES Magnetospheric Electron Detector
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='maged', trange=trange, probe=probe, datatype=datatype, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def magpd(trange=['2013-11-5', '2013-11-6'], 
        probe='15',
        datatype='1min', 
        suffix='',  
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GOES Magnetospheric Proton Detector
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='magpd', trange=trange, probe=probe, datatype=datatype, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def hepad(trange=['2013-11-5', '2013-11-6'], 
        probe='15',
        datatype='1min', 
        suffix='',  
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GOES High energy Proton and Alpha Detector
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='hepad', trange=trange, probe=probe, datatype=datatype, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def xrs(trange=['2013-11-5', '2013-11-6'], 
        probe='15',
        datatype='1min', 
        suffix='',  
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GOES X-ray Sensor
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='xrs', trange=trange, probe=probe, datatype=datatype, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)
