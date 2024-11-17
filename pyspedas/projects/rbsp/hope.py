from .load import load


def hope(trange=['2015-11-5', '2015-11-6'],
         probe='a',
         datatype='moments',
         level='l3',
         rel='rel04',
         prefix='',
         suffix='',
         force_download=False,
         get_support_data=False,
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the Energetic Particle, Composition, and Thermal Plasma Suite (ECT)

    Parameters
    ----------
        trange : list of str, default=['2015-11-5', '2015-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name: 'a' or 'b'

        datatype : str, default='moments'
            Data type. Valid options are specific to different data levels.

        level : str, default='l3'
            Data level. Valid options: 'l1', 'l2', 'l3', 'l4'

        rel : str, default='rel04'
            Release version of the data.

        prefix : str, optional
            The tplot variable names will be given this prefix. By default, no prefix is added.

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        force_download : bool, default=False
            Download file even if local version is more recent than server version.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> hope_vars = pyspedas.projects.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')
    >>> tplot('Ion_density')
    """

    return load(instrument='hope', rel=rel, trange=trange, probe=probe, datatype=datatype, level=level, prefix=prefix, suffix=suffix, force_download=force_download, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)
