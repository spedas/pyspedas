from pytplot import options
from .load import load


def swa(trange=['2020-07-22', '2020-07-23'],
        datatype='pas-eflux', 
        level='l2', 
        suffix='',  
        prefix='',
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Solar Wind Plasma Analyser (SWA)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        level: str
            Data level (default: l2)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no prefix is added.
            Default: ''
        
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """

    if prefix is None:
        prefix = ''
    
    if suffix is None:
        suffix = ''

    loaded_vars = load(instrument='swa', trange=trange, level=level, datatype=datatype, suffix=suffix, prefix=prefix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)
    
    if loaded_vars is None or notplot or downloadonly:
        return loaded_vars

    if prefix+'eflux'+suffix in loaded_vars:
        options(prefix+'eflux'+suffix, 'spec', True)
        options(prefix+'eflux'+suffix, 'ylog', True)
        options(prefix+'eflux'+suffix, 'zlog', True)

    return loaded_vars


