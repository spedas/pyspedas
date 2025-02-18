from .load import load

# Refer to __init__.py for revision history before load routines split out into separate files

def vefi(trange=['2010-11-5', '2010-11-6'],
        datatype='efield_1sec',
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
    This function loads data from the Vector Electric Field Instrument (VEFI)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2010-11-5', '2010-11-6']

        datatype: str
            String specifying datatype (options: 'efield_1sec', 'bfield_1sec', 'ld_500msec')
            Default: 'efield_1sec'

        prefix: str
            The tplot variable names will be given this prefix.
            Default: '', no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.
            Default: '', no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data". 

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted. 
            Default: None. All variables are loaded in.

        varnames: list of str
            List of variable names to load
            Default: []. If not specified, all data variables are loaded

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
        List of tplot variables created.

        
    Example:
    ----------
        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> vefi_vars = pyspedas.projects.cnofs.vefi(trange=['2013-11-5', '2013-11-6'])
        >>> tplot(['E_meridional', 'E_zonal'])
    """
    return load(instrument='vefi', datatype=datatype, trange=trange, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)


