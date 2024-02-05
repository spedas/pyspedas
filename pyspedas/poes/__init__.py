from .load import load
from pyspedas.utilities.datasets import find_datasets


def sem(trange=['2018-11-5', '2018-11-6'], 
        probe=['noaa19'],
        datatype=None,
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads POES Space Environment Monitor (SEM) data
    
    Parameters
    ----------
        trange : list of str, default=['2018-11-5', '2018-11-6']
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str, default=['noaa19']
            POES spacecraft name(s); e.g., metop1, metop2, noaa15, noaa16,
            noaa18, noaa19

        datatype: str, optional
            This variable is unused. It is reserved for the future use.

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str, default=False
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    dict or list
        List of tplot variables created.

    Examples
    --------
    >>> sem_vars = pyspedas.poes.sem(trange=['2013-11-5', '2013-11-6'])
    >>> tplot('ted_ele_tel30_low_eflux')
    """
    return load(instrument='sem', probe=probe, trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def datasets(instrument=None, label=True):
    return find_datasets(mission='POES', instrument='sem2', label=label)
