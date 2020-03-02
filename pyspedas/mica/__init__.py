
from .load import load

def induction(site=None, 
              trange=['2019-02-01','2019-02-02'],
              suffix='',  
              get_support_data=False, 
              varformat=None,
              downloadonly=False,
              notplot=False,
              no_update=False,
              time_clip=False):
    """
    This function loads data from the Magnetic Induction Coil Array (MICA)
    
    Parameters:
        site: str
            abbreviated name of station. sites include:
            NAL, LYR, LOR, ISR, SDY, IQA, SNK, MCM, SPA, JBS, NEV, HAL, PG2[3,4,5]

        trange: list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

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

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns:
        List of tplot variables created.

    """
    return load(site=site, trange=trange, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)
