from .load import load

# This routine was moved out of __init__.py.  Please see that file for previous revision history.


def imager(trange=['2018-11-5', '2018-11-6'], 
        probe='1',
        datatype='',
        prefix='',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        force_download=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads TWINS imager data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options: ''
            Default: ''

        prefix: str
            The tplot variable names will be given this prefix.
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: '' (all variables loaded)

        varnames: list of str
            List of variable names to load
            Default: [] (all variables will be loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables
            Default: False

        force_download: bool
            Set this flag to download the CDF files, even if the local copy is newer
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

    Returns
    --------
        list of str
            List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> img_vars = pyspedas.projects.twins.imager(trange=['2018-11-5', '2018-11-6'])
    >>> tplot('smooth_image_val')

    """
    return load(instrument='imager', trange=trange, probe=probe, datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, force_download=force_download, notplot=notplot, time_clip=time_clip, no_update=no_update)


