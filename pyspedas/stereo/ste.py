from .load import load

# This routine was originally in stereo/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

def ste(trange=['2013-11-5', '2013-11-6'],
        probe='a',
        level='l1',
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
    This function loads data from the Suprathermal Electron Telescope

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        probe: str
            Spacecraft probe ('a' for ahead, 'b' for behind)
            Default: 'a'

        level: str
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: '', no suffix is added.

        prefix: str
            The tplot variable names will be given this prefix.
            Default: '', no prefix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False. Only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None. All variables are loaded in.

        varnames: list of str
            List of variable names to load.
            Default: [], if not specified, all data variables are loaded

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

    Returns
    ----------
        List of tplot variables created.

    """

    return load(instrument='ste', trange=trange, probe=probe, suffix=suffix, prefix=prefix, level=level,
                get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                notplot=notplot, time_clip=time_clip, no_update=no_update)

