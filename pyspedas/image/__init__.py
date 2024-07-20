from .load import load
from pyspedas.utilities.datasets import find_datasets


def lena(
    trange=["2004-11-5", "2004-11-6"],
    datatype="k0",
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
    Loads IMAGE LENA data.

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
        instrument="lena",
        trange=trange,
        datatype=datatype,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def mena(
    trange=["2004-11-5", "2004-11-6"],
    datatype="k0",
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
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def hena(
    trange=["2004-11-5", "2004-11-6"],
    datatype="k0",
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
    Loads IMAGE HENA data.

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
        instrument="hena",
        trange=trange,
        datatype=datatype,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def rpi(
    trange=["2004-11-5", "2004-11-6"],
    datatype="k0",
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
    Loads IMAGE RPI data.

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
        instrument="rpi",
        trange=trange,
        datatype=datatype,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def euv(
    trange=["2004-11-5", "2004-11-6"],
    datatype="k0",
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
    Loads IMAGE EUV data.

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
        instrument="euv",
        trange=trange,
        datatype=datatype,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def fuv(
    trange=["2004-11-5", "2004-11-6"],
    datatype="k0",
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
    Loads IMAGE FUV data.

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
        instrument="fuv",
        trange=trange,
        datatype=datatype,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def orbit(
    trange=["2004-11-5", "2004-11-6"],
    datatype="def_or",
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
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def datasets(instrument=None, label=True):
    return find_datasets(mission="IMAGE", instrument=instrument, label=label)
