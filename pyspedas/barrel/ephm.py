from .load import load

def ephm(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        no_update=False,
        time_clip=False,
        force_download=False):
    """
    This function load data from BARREL Ephemeris (GPS data and magnetic coordinates)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-01-29','2013-01-30']

        probe: str
            Options::

                '1a'...'1v'
                '2a'...'2y'
                '3a'...'3g'
                '4a'...'4f'
                '5a'
                '6a'
                '7a'

            Default: '1A'

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables.
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
        List of tplot variables created.

    Example:
    ----------
        >>> import pyspedas
        >>> from pytplot import tplot
        >>> pyspedas.barrel.ephm(trange=['2013-01-29','2013-01-30'], probe='1A')
        >>> tplot('brl1A_GPS_Lat')
    """
   
    return load(datatype='ephm', trange=trange, probe=probe, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update, force_download=force_download)


