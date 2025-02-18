from .load import load
from pytplot import options
from pyspedas.utilities.datasets import find_datasets

# This routine was originally in ace/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

def epam(trange=['2018-11-5', '2018-11-6'],
        datatype='k0',
        prefix='',
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
    Load data from the ACE Electron Proton Alpha Monitor (EPAM)
    
    Parameters
    ----------

        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        datatype: str

            Data type; Valid options::

                h1: 5-Minute Level 2 Data
                h2: 1-Hour Level 2 Data
                h3: 12-second Level 2 Data
                k0: (default) 5-Minute Key Parameters
                k1: 1-Hour Key Parameters

            Default: 'k0'

        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
            Default: None

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)
            Default: []

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

        list of str
            List of the tplot variables created.
    
    Examples
    ----------

        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> epam_vars = pyspedas.projects.ace.epam(trange=['2018-11-5', '2018-11-6'])
        >>> tplot(['H_lo', 'Ion_very_lo', 'Ion_lo', 'Ion_mid', 'Ion_hi', 'Electron_lo', 'Electron_hi'])

    """
    return load(trange=trange, instrument='epm', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, downloadonly=downloadonly, notplot=notplot, no_update=no_update, varnames=varnames,
                time_clip=time_clip, force_download=force_download)


