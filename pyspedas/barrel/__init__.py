from .load import load
from .spec import bg_sub

def sspc(trange=['2013-01-28', '2013-01-29'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads the Slow Spectrum (256s) CDF files stored at CDAWeb for a specific payload
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Balloon flight ID. See README.md for information about different flights.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        no_update: bool
            If set, only load data from your local cache

    Returns:
        List of tplot variables created.

    """
    return load(datatype='sspc', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def mspc(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads the Medium Spectrum (42s) CDF files stored at CDAWeb for a specific payload
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Balloon flight ID. See README.md for information about different flights.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        no_update: bool
            If set, only load data from your local cache

    Returns:
        List of tplot variables created.

    """
    return load(datatype='mspc', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def fspc(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads the Fast Spectrum (also called Light Curve) CDF files stored at CDAWeb for a specific payload
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Balloon flight ID. See README.md for information about different flights.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        no_update: bool
            If set, only load data from your local cache

    Returns:
        List of tplot variables created.

    """
    return load(datatype='fspc',trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def rcnt(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads the Rate Counter (scintillator statistics) CDF files stored at CDAWeb for a specific payload
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Balloon flight ID. See README.md for information about different flights.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        no_update: bool
            If set, only load data from your local cache

    Returns:
        List of tplot variables created.

    """
    return load(datatype='rcnt', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def magn(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads the Magnetometer CDF files stored at CDAWeb for a specific payload
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Balloon flight ID. See README.md for information about different flights.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        no_update: bool
            If set, only load data from your local cache

    Returns:
        List of tplot variables created.

    """
    return load(datatype='magn', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)

def ephm(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads the Ephemeris CDF files stored at CDAWeb for a specific payload.
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Balloon flight ID. See README.md for information about different flights.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        no_update: bool
            If set, only load data from your local cache
        
        dl_folder: str
            Alternative name for the data folder in CDAWeb. Generally this is the same value as `datatype`
            but Ephemeris files are currently stored in the `ephem` folder instead of `ephm` (except for 1N for some reason)

    Returns:
        List of tplot variables created.

    """
    
    dl_folder = "ephem" if probe.upper() != "1N" else "ephm"
    return load(datatype='ephm', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update, dl_folder=dl_folder)

def hkpg(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False):
    """
    This function loads the Housekeeping CDF files stored at CDAWeb for a specific payload
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Balloon flight ID. See README.md for information about different flights.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        no_update: bool
            If set, only load data from your local cache

    Returns:
        List of tplot variables created.

    """
    return load(datatype='hkpg', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update)
