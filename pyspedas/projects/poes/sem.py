from .load import load

# This routine was originally in poes/__init__.py.
def sem(trange=['2018-11-5', '2018-11-6'],
        probe=['noaa19'],
        datatype=None,
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
    This function loads POES Space Environment Monitor (SEM) data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        probe: str or list of str
            POES spacecraft name(s); e.g., metop1, metop2, noaa15, noaa16,
            noaa18, noaa19. Default: noaa19

        datatype: str, optional
            This variable is unused. It is reserved for the future use.

        prefix: str
            The tplot variable names will be given this prefix.  By default, no prefix is added.
            Default: ''

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool, default=False
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. Default: False

        varformat: str
            If specified,  file variable formats to load into tplot.  Wildcard characters
            `*` and `?` are accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables. Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables. Default: False

        no_update: bool
            If set, only load data from your local cache. Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword. Default: False

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False

    Returns
    -------
    dict or list
        List of tplot variables created.

    Examples
    --------
    >>> sem_vars = pyspedas.poes.sem(trange=['2013-11-5', '2013-11-6'])
    >>> tplot('ted_ele_tel30_low_eflux')
    """
    return load(instrument='sem', probe=probe, trange=trange, datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)
