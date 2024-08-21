from .load import load

# This routine was originally in geotail/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

def cpi(trange=['2018-11-5', '2018-11-6'],
        datatype='k0',
        suffix='',
        prefix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        force_download=False):
    """
    This function loads data from the CPI instrument

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        prefix: str
            The tplot variable names will be given this prefix.
            Default: no prefix is added

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

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='cpi', trange=trange, datatype=datatype, suffix=suffix, prefix=prefix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip,
                no_update=no_update, force_download=force_download)
