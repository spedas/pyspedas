import logging
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from .config import CONFIG


def load(
    trange=["2018-10-16", "2018-10-17"],
    instrument="mag",
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
    Load DSCOVR data into tplot variables.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ['2018-10-16', '2018-10-17'].
    instrument : str or list of str, optional
        Type of instrument.
        Values can be: 'mag', 'fc' or 'faraday_cup', 'orbit' or 'orb' or 'pre_or', 'att' or 'def_at', 'pre_at', 'all'.
        If 'all' is specified, all instruments will be loaded.
        Default is 'mag'.
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
    >>> mag_vars = pyspedas.projects.dscovr.mag(trange=['2018-11-5', '2018-11-6'])
    >>> tplot('dsc_h0_mag_B1GSE')
    """

    out_files = []
    out_vars = []

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
        instrument = ["mag", "fc", "orb", "def_at", "pre_at", "pre_or"]

    for instr in instrument:
        if instr == "mag":
            pathformat = "h0/mag/%Y/dscovr_h0_mag_%Y%m%d_v??.cdf"
            pre = "dsc_h0_mag_"
        elif instr == "faraday_cup" or instr == "fc":
            pathformat = "h1/faraday_cup/%Y/dscovr_h1_fc_%Y%m%d_v??.cdf"
            pre = "dsc_h1_fc_"
        elif instr == "def_at" or instr == "att":
            pathformat = "orbit/def_at/%Y/dscovr_at_def_%Y%m%d_v??.cdf"
            pre = "dsc_att_"
        elif instr == "pre_at":
            # Only for year: 2015, 2016, 2017
            pathformat = "orbit/pre_at/%Y/dscovr_at_pre_%Y%m%d_v??.cdf"
            pre = "dsc_at_pre_"
        elif instr in ["pre_or", "orb", "orbit"]:
            pathformat = "orbit/pre_or/%Y/dscovr_orbit_pre_%Y%m%d_v??.cdf"
            pre = "dsc_orbit_"
        else:
            logging.error("Invalid instrument type: " + instr)
            continue

        # If prefix is not empty, add it to the pre variable
        if prefix != "":
            pre = prefix + pre

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

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
