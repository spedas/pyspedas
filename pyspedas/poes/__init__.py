
from .load import load

def sem(trange=['2018-11-5', '2018-11-6'], 
        probe=['noaa19'],
        datatype='*', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False):
    """
    This function loads Parker Solar Probe FIELDS data
    
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
    return load(instrument='sem', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly)
