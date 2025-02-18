from .load import load
from typing import List, Union, Optional


def wbd(trange:List[str]=['2003-11-01/14:00:00','2003-11-01/14:05:00'],
        probe:Union[str,List[str]]='1',
        datatype:str='waveform',
        prefix:str='',
        suffix:str='',
        get_support_data:bool=False,
        varformat:str=None,
        varnames:List[str]=[],
        downloadonly:bool=False,
        notplot:bool=False,
        no_update:bool=False,
        time_clip:bool=False,
        force_download=False) -> List[str]:
    """
    Load data from the Cluster Wide Band Data receiver
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2003-11-01/14:00:00','2003-11-01/14:05:00']

        probe: list of str
            List of probes to load.  Valid options: '1','2','3','4'
            Default: '1'

        datatype: str
            Data type; Valid options:
            Default: 'waveform'

        prefix: str
            The tplot variable names will be given this prefix.
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            If True, Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted. If empty or None, all variables will be loaded.
            Default: None (all variables loaded)

        varnames: list of str
            List of CDF variable names to load (if empty or not specified,
            all data variables are loaded)
            Default: [] (all variables loaded)

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
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> wbd_vars = pyspedas.projects.cluster.wbd(trange=['2003-11-01/14:00:00','2003-11-01/14:05:00'],probe=['1'])
    >>> # Note lack of probe IDs in the variables loaded -- only load one probe at a time
    >>> tplot('WBD_Elec')
    """
    return load(instrument='wbd', trange=trange, probe=probe, datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


