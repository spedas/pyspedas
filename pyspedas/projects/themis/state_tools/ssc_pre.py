from pyspedas.projects.themis.load import load


def ssc_pre(
    trange=["2026-03-23", "2026-03-24"],
    probe="c",
    level="l2",
    suffix="",
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    time_clip=True,
):
    """
    Load THEMIS predicted orbit data from CDAWeb/SSCWeb (Satellite Situation Center).

    For example: https://cdaweb.gsfc.nasa.gov/pub/data/themis/thc/ssc_pre/
    Each downloaded file contains data for a full year.

    See also, pyspedas.projects.themis.state_tools.ssc

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-03-23', '2017-03-24']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')
            Default: 'c'

        level: str
            Data type; Default: 'l2'; Unused.

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False; only loads data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None; all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list, so all data variables are loaded

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
            Time clip the variables to exactly the range specified
            in the trange keyword
            Default: True

    Returns
    -------
    List of str
        List of tplot variables created
        Empty list if no data

    Example
    -------
        >>> from pyspedas.projects.themis import ssc_pre
        >>> vars = ssc_pre(probe='d', trange=['2026-12-25', '2026-12-26'])
        >>> print(vars)


    """
    return load(
        instrument="ssc_pre",
        trange=trange,
        level=level,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        probe=probe,
        time_clip=time_clip,
        no_update=no_update,
    )
