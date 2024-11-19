from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(
    trange=["2007-11-01", "2007-11-02"],
    instrument="mpa",
    probe="a1",
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
    Loads LANL data for the specified instrument and probe.

    Can load data from two instruments, the Magnetospheric Plasma Analyzer (mpa) and the Synchronous Orbit Particle Analyzer (spa).

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
        Valid datatypes: 'k0', 'h0'.
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


    # remote directory names
    LANL_SC = {
        "l0": "90",
        "l1": "91",
        "l4": "94",
        "l7": "97",
        "l9": "89",
        "a1": "01a",
        "a2": "02a",
    }
    probe = probe.lower()

    # h0 is only available for mpa and has a different directory structure
    datatypestr = ""
    if datatype == "h0" and instrument == "mpa":
        datatypestr = "_h0"

    # path for SPDF files
    pathformat = (
        LANL_SC[probe]
        + datatypestr
        + "_"
        + instrument
        + "/%Y/"
        + probe
        + "_"
        + datatype
        + "_"
        + instrument
        + "_%Y%m%d_v??.cdf"
    )

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(
        remote_file=remote_names,
        remote_path=CONFIG["remote_data_dir"],
        local_path=CONFIG["local_data_dir"],
        no_download=no_update,
        force_download=force_download
    )
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(
        out_files,
        prefix=prefix,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        notplot=notplot,
    )

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix="")

    return tvars
