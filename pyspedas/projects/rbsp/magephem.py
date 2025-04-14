from .load import load


# Add the loader for MagEphem cdf files.
def magephem(trange=["2018-11-5", "2018-11-6"], probe="a", cadence="1min", coord="op77q", prefix="", suffix="", force_download=False, get_support_data=False, varformat=None, varnames=[], downloadonly=False, notplot=False, no_update=False, time_clip=False):  # 1 min or 5 min  # op77q, t89d, t89q, and ts04d
    """
    This function loads the Mag Ephemeris data for the Van Allen Probes
    The data is available from:
    https://spdf.gsfc.nasa.gov/pub/data/rbsp/rbspa/ephemeris

    Parameters
    ----------
        trange : list of str, default=['2018-11-5', '2018-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name: 'a' or 'b'

        cadence : str, default='1min'
            Data cadence; options: '1min', '5min'

        coord : str, default='op77q'
            Data coordinate system. options: 'op77q', 't89d', 't89q', and 'ts04d'

        prefix : str, optional
            The tplot variable names will be given this prefix. By default, no prefix is added.

        suffix : str, optional
            Suffix for tplot variable names. By default, no suffix is added.

        force_download : bool, default=False
            Download file even if local version is more recent than server version.

        get_support_data : bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat : str, optional
            The file variable formats to load into tplot. Wildcard character
            "*" is accepted. By default, all variables are loaded in.

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
    >>> magephem_vars = pyspedas.projects.rbsp.magephem(trange=['2018-11-5/10:00', '2018-11-5/15:00'], cadence='1min', coord='op77q', time_clip=True)
    >>> tplot(['L','Lsimple','Kp','Dst'])
    """
    return load(instrument="magephem", trange=trange, probe=probe, cadence=cadence, coord=coord, prefix=prefix, suffix=suffix, force_download=force_download, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def magephem_ect(trange=["2018-11-5", "2018-11-6"], probe="a", cadence="1min", coord="op77q", filetype="h5", prefix="", suffix="", force_download=False, get_support_data=False, varformat=None, varnames=[], downloadonly=False, notplot=False, no_update=False, time_clip=False):  # 1 min or 5 min  # op77q, t89d, t89q, and ts04d  # h5 or txt
    """
    @Author: Xiangning Chu, 2025-04-07
    Load magnetic field line mapping ephemeris data for the Van Allen Probes from the ECT website.

    This function retrieves and processes magnetic field line mapping data from the ECT website
    (https://rbsp-ect.newmexicoconsortium.org/data_pub/), which is particularly useful for periods
    when data is not available through CDAWeb. The data includes magnetic field line mapping parameters
    such as L-shell, MLT, and magnetic coordinates in various coordinate systems.

    Parameters
    ----------
    trange : list of str, default=['2018-11-5', '2018-11-6']
        Time range of interest [starttime, endtime] with the format:
        - ['YYYY-MM-DD', 'YYYY-MM-DD'] for daily ranges
        - ['YYYY-MM-DD/hh:mm:ss', 'YYYY-MM-DD/hh:mm:ss'] for specific time ranges

    probe : str or list of str, default='a'
        Spacecraft probe identifier: 'a' for RBSP-A or 'b' for RBSP-B

    cadence : str, default='1min'
        Temporal resolution of the data:
        - '1min': 1-minute resolution
        - '5min': 5-minute resolution

    coord : str, default='op77q'
        Magnetic coordinate system for the data:
        - 'op77q': Olson-Pfitzer quiet model
        - 't89d': Tsyganenko 1989 dynamic model
        - 't89q': Tsyganenko 1989 quiet model
        - 'ts04d': Tsyganenko-Sitnov 2004 dynamic model

    filetype : str, default='h5'
        File format for data retrieval:
        - 'h5': HDF5 format
        - 'txt': ASCII text format

    prefix : str, optional
        Prefix to be added to tplot variable names

    suffix : str, optional
        Suffix to be added to tplot variable names

    force_download : bool, default=False
        If True, forces download even if local version is more recent

    get_support_data : bool, default=False
        If True, loads support data (VAR_TYPE="support_data") into tplot

    varformat : str, optional
        File variable format to load into tplot (wildcard "*" accepted)

    varnames : list of str, optional
        Specific variable names to load (if empty, loads all variables)

    downloadonly : bool, default=False
        If True, downloads files without loading into tplot variables

    notplot : bool, default=False
        If True, returns data in hash tables instead of tplot variables

    no_update : bool, default=False
        If True, only loads data from local cache

    time_clip : bool, default=False
        If True, clips variables to exact time range specified in trange

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True

    Examples
    --------
    >>> # Load 1-minute resolution data in Olson-Pfitzer quiet coordinates
    >>> magephem_vars = pyspedas.projects.rbsp.magephem_ect(
    ...     trange=['2018-11-5/10:00', '2018-11-5/15:00'],
    ...     cadence='1min',
    ...     coord='op77q',
    ...     time_clip=True
    ... )
    >>> # Plot L-shell and magnetic coordinates
    >>> tplot(['L', 'Lsimple', 'Kp', 'Dst'])

    Notes
    -----
    - This function is particularly useful for periods when data is not available through CDAWeb
    - The data includes magnetic field line mapping parameters essential for radiation belt studies
    - Coordinate systems are based on different magnetic field models for various geomagnetic conditions
    """
    from pyspedas.utilities.dailynames import dailynames
    from pyspedas.utilities.download import download
    from pytplot import time_clip as tclip

    from .config import CONFIG_ECT
    from .magephem_read import magephem_read_h5, magephem_read_txt

    if not isinstance(probe, list):
        probe = [probe]

    out_files = []

    if notplot:
        tvars = {}
    else:
        tvars = []

    if prefix is None:
        prefix = ""

    if suffix is None:
        suffix = ""

    for prb in probe:

        remote_path = CONFIG_ECT["remote_data_dir"]
        local_path = CONFIG_ECT["local_data_dir"]

        pathformat = "rbsp" + prb + "/MagEphem/definitive" + "/%Y/rbsp" + prb + "_def_MagEphem_" + coord.upper() + "_%Y%m%d_v*." + filetype

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)
        files = download(remote_file=remote_names, remote_path=remote_path, local_path=local_path, no_download=no_update, force_download=force_download)
        if files:
            out_files.extend(files)

        if not downloadonly:
            if filetype == "h5":
                tvars_o = magephem_read_h5(sorted(files), varnames=varnames, notplot=notplot, prefix=prefix, suffix=suffix)
            elif filetype == "txt":
                tvars_o = magephem_read_txt(sorted(files), varnames=varnames, notplot=notplot, prefix=prefix, suffix=suffix)

            if notplot:
                tvars.update(tvars_o)
            else:
                tvars.extend(tvars_o)

    if downloadonly:
        return sorted(out_files)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix="")

    return tvars
