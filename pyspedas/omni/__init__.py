
from .load import load

def data(trange=['2013-11-5', '2013-11-6'],
        datatype='1min',
        level='hro2',
        suffix='',  
        get_support_data=False, 
        get_ignore_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=True):
    """
    This function loads OMNI (Combined 1AU IP Data; Magnetic and Solar Indices) data
    
    Parameters
    ----------
        trange: list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
        
        level: str
            Data level; valid options: hro, hro2

        datatype: str
            Data type; valid options: 1min, 5min, hourly (1 hour)

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

    Returns
    ----------
        List of tplot variables created.

    """
    return load(trange=trange, level=level, datatype=datatype, suffix=suffix, 
                get_support_data=get_support_data, get_ignore_data=get_ignore_data,varformat=varformat, 
                varnames=varnames, downloadonly=downloadonly, notplot=notplot, 
                time_clip=time_clip, no_update=no_update)
