from .load import load

# This routine was originally in image/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

def orbit(
    trange=["2004-11-5", "2004-11-6"],
    datatype="def_or",
    suffix='',
    prefix='',
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    time_clip=False,
    force_download=False,
):
    """
    Loads IMAGE orbit data.

    Parameters
    ----------
    trange : list of str
        Time range of interest with the format ['YYYY-MM-DD','YYYY-MM-DD'] or
        to specify more or less than a day ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
    datatype : str
        Data type. Valid options are not specified in the function signature.
    suffix : str, optional
        The tplot variable names will be given this suffix. By default, no suffix is added.
    prefix : str, optional
        The tplot variable names will be given this prefix. By default, no prefix is added.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        By default, only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot. Wildcard character "*" is accepted.
        By default, all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load. If not specified, all data variables are loaded.
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables.
    no_update : bool, optional
        If set, only load data from your local cache.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------
    list
        List of tplot variables created.
    """
    return load(
        instrument="orbit",
        trange=trange,
        datatype=datatype,
        suffix=suffix,
        prefix=prefix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )
