from .load import load

# This routine was originally in image/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

def mena(
    trange=["2004-11-5", "2004-11-6"],
    datatype="k0",
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
    Loads IMAGE MENA data.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest with the format ['YYYY-MM-DD','YYYY-MM-DD'] or
        to specify more or less than a day ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Defaults to ['2004-11-5', '2004-11-6'].
    datatype : str, optional
        Data type. Defaults to 'k0'.
    suffix : str, optional
        The tplot variable names will be given this suffix. Defaults to ''.
    prefix : str, optional
        The tplot variable names will be given this prefix. Defaults to ''.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        By default, only loads in data with a "VAR_TYPE" attribute of "data". Defaults to False.
    varformat : str, optional
        The file variable formats to load into tplot. Wildcard character "*" is accepted.
        By default, all variables are loaded in. Defaults to None.
    varnames : list of str, optional
        List of variable names to load. If not specified, all data variables are loaded. Defaults to [].
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables. Defaults to False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables. Defaults to False.
    no_update : bool, optional
        If set, only load data from your local cache. Defaults to False.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword. Defaults to False.
    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------
    list
        List of tplot variables created.
    """
    return load(
        instrument="mena",
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
