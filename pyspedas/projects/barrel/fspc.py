from .load import load

# This routine was moved out of __init__.py.  Please see that file for previous revision history.

def fspc(trange=['2013-01-29','2013-01-30'],
        probe='1A',
        downloadonly=False,
        prefix='',
        suffix='',
        no_update=False,
        time_clip=False,
        force_download=False):
    """
    This function load data from BARREL Fast Spectra (4 channels record at 20Hz)

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

        prefix: str
            This string will be prepended to the tplot variable names created. Default: ''

        suffix: str
            This string will be appended to the tplot variable names created.  Default: ''

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
        >>> from pyspedas import tplot
        >>> pyspedas.projects.barrel.fspc(trange=['2013-01-17', '2013-01-19'], probe='1D')
        >>> tplot('brl1D_FSPC1')
    """

    return load(datatype='fspc',trange=trange, probe=probe,  prefix=prefix, suffix=suffix, downloadonly=downloadonly, time_clip=time_clip, no_update=no_update, force_download=force_download)


