from .load import load

# This routine was originally in lanl/__init__.py.
def spa(
    trange=["2004-10-31", "2004-11-01"],
    probe="l1",
    datatype="k0",
    prefix="",
    suffix="",
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
    Load data from the LANL Synchronous Orbit Particle Analyzer (SPA)

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest with the format ['YYYY-MM-DD','YYYY-MM-DD'] or
        to specify more or less than a day ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Defaults to ['2004-10-31', '2004-11-01'].
    instrument : str, optional
        The instrument to load data for. Defaults to 'mpa'.
        Valid instruments: 'mpa', 'spa'.
    probe : str, optional
        The probe to load data for. Defaults to 'a1'.
        Valid probes (with gaps for some dates): 'l0', 'l1', 'l4', 'l7', 'l9', 'a1', 'a2'.
    datatype : str, optional
        The datatype. Defaults to 'k0'.
        Valid datatypes: 'k0'
        Data for 'h0' datatype is available only for the 'mpa' instrument and only for a few days in 1998.
    prefix : str, optional
        The tplot variable names will be given this prefix. By default, no prefix is added.
        Defaults to ''.
    suffix : str, optional
        The tplot variable names will be given this suffix. Defaults to ''.
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
    force_download : bool
        Download file even if local version is more recent than server version. Defaults to False.

    Returns
    -------
    list
        List of tplot variables created.
    """

    tvars = load(
        instrument="spa",
        trange=trange,
        datatype="k0",
        probe=probe,
        prefix=prefix,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download
    )

    if tvars is None or notplot or downloadonly:
        return tvars

    return tvars
