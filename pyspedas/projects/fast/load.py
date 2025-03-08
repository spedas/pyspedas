import logging
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(
    trange=["1996-12-01", "1996-12-02"],
    instrument="dcf",
    datatype="",
    level="l2",
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
    Load FAST data into tplot variables.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ["1996-12-01", "1996-12-02"].
    instrument : str or list of str, optional
        Type of instrument.
        Values can be: 'dcf', 'acf', 'esa', 'teams', 'all'.
        If 'all' is specified, all instruments will be loaded.
        Default is 'dcf'.
    datatype : str, optional
        Data type to load. Depends on the instrument.
        For 'esa' valid options are: 'eeb', 'ees', 'ieb', 'ies'.
        For all other insturments, this keyword is ignored.
        Default is ''.
    level : str, optional
        Data level to load. Depends on the instrument.
        For 'dcf' and 'teams' valid options are: 'l2', 'k0'.
        For all other instruments, this keyword is ignored.
        Default is 'l2'.
    prefix : str, optional
        The tplot variable names will be given this prefix.
        Default is ''.
        In all cases a suitable prefix will be given depending on the instrument.
    suffix : str, optional
        The tplot variable names will be given this suffix.
        Default is no suffix is added.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        Default is False; only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        Default is all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load.
        Default is all data variables are loaded.
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables.
        Default is False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables.
        Default is False.
    no_update : bool, optional
        If set, only load data from your local cache.
        Default is False.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
        Default is False.
    force_download : bool, optional
        Download file even if local version is more recent than server version.
        Default is False.

    Returns
    -------
    list of str/dictionary
        List of tplot variables created.
        If downloadonly is set to True, returns a list of the downloaded files.
        If notplot is set to True, returns a dictionary of the data loaded.

    Examples
    --------
    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> dcf_vars = pyspedas.projects.fast.dcf(trange=["1996-12-01", "1996-12-02"])
    >>> tplot(['fast_dcf_DeltaB_GEI'])
    >>> acf_vars = pyspedas.projects.fast.acf(trange=["1996-12-01", "1996-12-02"])
    >>> tplot('fast_acf_HF_E_SPEC')
    >>> esa_vars = pyspedas.projects.fast.esa(trange=["1996-12-01", "1996-12-02"])
    >>> tplot('fast_esa_eflux')
    >>> teams_vars = pyspedas.projects.fast.teams(trange=["2005-08-01", "2005-08-02"])
    >>> tplot(['fast_teams_helium_omni_flux'])
    """

    out_files = []
    out_vars = []
    file_resolution = 24 * 3600.0

    if (
        trange is None
        or not isinstance(trange, list)
        or len(trange) != 2
        or trange[0] > trange[1]
    ):
        logging.error("Invalid trange specified.")
        return out_vars

    if not isinstance(instrument, list):
        instrument = [instrument]
    if "all" in instrument:
        instrument = ["dcf", "acf", "esa", "teams"]

    pathformat = ""
    for instr in instrument:
        if instr == "dcf":
            # levels are l2 (1996-1998) or k0 (1996-2002)
            if level == "k0":
                pathformat = "dcf/k0/%Y/fa_k0_dcf_%Y%m%d_v??.cdf"
            else:
                pathformat = "dcf/l2/dcb/%Y/%m/fast_hr_dcb_%Y%m%d%H????_?????_v??.cdf"
                file_resolution = 3600.0
        elif instr == "acf":
            # level k0 only (1996-2002)
            pathformat = "acf/k0/%Y/fa_k0_acf_%Y%m%d_v??.cdf"
        elif instr == "esa":
            # level l2 only
            # datatypes are eeb, ees, ieb, ies (1996-2009)
            if datatype not in ["eeb", "ees", "ieb", "ies"]:
                datatype = "eeb"  # default
            pathformat = (
                "esa/l2/"
                + datatype
                + "/%Y/%m/fa_esa_l2_"
                + datatype
                + "_%Y%m%d??????_*_v??.cdf"
            )
        elif instr == "teams":
            # levels are l2 (1996-2009) or k0 (1996-2009)
            if level == "k0":
                # no datatype for k0 data
                pathformat = "teams/k0/%Y/fa_k0_tms_%Y%m%d_v??.cdf"
            else:
                # for l2 data, the only available datatype is "pa"
                pathformat = "teams/l2/pa/%Y/%m/fast_teams_pa_l2_%Y%m%d_?????_v??.cdf"

        else:
            logging.error("Invalid instrument type: " + instr)
            continue

        # If prefix is not empty, add it to the pre variable
        pre = "fast_" + instr + "_"
        if prefix != "":
            pre = prefix + pre

        # find the full remote path names using the trange
        remote_names = dailynames(
            file_format=pathformat, trange=trange, res=file_resolution
        )

        # download the files
        files = download(
            remote_file=remote_names,
            remote_path=CONFIG["remote_data_dir"],
            local_path=CONFIG["local_data_dir"],
            no_download=no_update,
            force_download=force_download,
        )
        if files is not None:
            if not isinstance(files, list):
                files = [files]
            out_files.extend(files)

        if not downloadonly and len(files) > 0:
            # Read the files into tplot variables
            vars = cdf_to_tplot(
                files,
                prefix=pre,
                suffix=suffix,
                get_support_data=get_support_data,
                varformat=varformat,
                varnames=varnames,
                notplot=notplot,
            )
            if not isinstance(vars, list):
                vars = [vars]
            out_vars.extend(vars)

    out_files = list(set(out_files))
    out_files = sorted(out_files)

    if not downloadonly and len(out_files) < 1:
        logging.info("No files were downloaded.")
        return out_files  # return an empty list

    if downloadonly:
        return out_files

    if notplot:
        if len(out_vars) < 1:
            logging.info("No variables were loaded.")
            return {}
        else:
            return out_vars[0]  # return data in hash tables

    if time_clip:
        tclip(out_vars, trange[0], trange[1], suffix="", overwrite=True)

    return out_vars
