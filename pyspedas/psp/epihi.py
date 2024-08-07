
from .load import load
from .filter import filter_fields

from pytplot import options, data_quants

# Loading
def epihi(trange=['2018-11-5', '2018-11-6'], 
        datatype='let1_rates1h', 
        level='l2',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        last_version=False):
    """
    This function loads Parker Solar Probe ISoIS/EPI-Hi data
    
    Parameters
    ----------
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

        last_version: bool
            If True, only download the highest-numbered file version

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='epihi', trange=trange, datatype=datatype, level=level, 
        suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update,last_version=last_version)

