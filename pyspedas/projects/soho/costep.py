from .load import load
from .costep_postprocessing import costep_postprocessing

def costep(trange=['2006-06-01', '2006-06-02'],
        datatype='ephin_l3i-1day',
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
    This function loads data from the Comprehensive Suprathermal and Energetic Particle Analyzer (COSTEP)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; options: (default: ephin_l3i-1day)
                    ephin_l3i-1day
                    ephin_l3i-1hr
                    ephin_l3i-30min
                    ephin_l3i-10min
                    ephin_l3i-5min
                    ephin_l3i-1min
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
    tvars= load(instrument='costep', trange=trange, datatype=datatype, suffix=suffix, prefix=prefix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return costep_postprocessing(tvars)


