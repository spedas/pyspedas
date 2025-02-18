import logging
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(
    trange=["1998-04-06", "1998-04-07"],
    instrument="mam",
    datatype="pp",
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
    Load data from the Equator-S mission.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ['1998-04-06', '1998-04-07'].
    instrument : str, list of str, optional
        Type of instrument.
        Valid values: 'aux', 'edi', 'epi',  'ici', 'mam', 'pcd', 'sfd', 'all'.
        Default is 'mam'.
        If 'all' is specified, all instruments will be loaded.
    datatype : str, optional
        Type of data.
        Default is 'pp'.
        Valid values:
        -- 'pp' for instruments: 'aux', 'edi', 'epi',  'ici', 'mam', 'pcd'
        -- 'sp' for instruments: 'sfd', 'edi'
        Instrument 'edi' has both 'pp' and 'sp' data; for all other instruments, datatype is ignored.
    prefix: str, optional
        The tplot variable names will be given this prefix.
        Default is ''.
    suffix : str, optional
        The tplot variable names will be given this suffix.
        Default is ''.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        Default is False, only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        Default is None, all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load.
        Default is [], all data variables are loaded.
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
    >>> edi_vars = pyspedas.equator_s.edi(trange=['1998-04-06', '1998-04-07'])
    >>> print(edi_vars)
    ['V_ed_xyz_gse%eq_pp_edi', 'E_xyz_gse%eq_pp_edi']
    >>> tplot(edi_vars)
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
        instrument = ["aux", "edi", "epi", "ici", "mam", "pcd", "sfd"]

    for instr in instrument:

        if instr == "aux":
            pathformat = "pp/aux/%Y/eq_pp_aux_%Y%m%d_v??.cdf"
        elif instr == "edi":
            # this is the only case that datatype is not predetermined
            # it can be either 'pp' or 'sp'
            if datatype == "sp":
                pathformat = "sp/edi/%Y/eq_sp_edi_%Y%m%d_v??.cdf"
            else:
                pathformat = "pp/edi/%Y/eq_pp_edi_%Y%m%d_v??.cdf"
        elif instr == "epi":
            pathformat = "pp/epi/%Y/eq_pp_epi_%Y%m%d_v??.cdf"
        elif instr == "ici":
            pathformat = "pp/ici/%Y/eq_pp_ici_%Y%m%d_v??.cdf"
        elif instr == "mam":
            pathformat = "pp/mam/%Y/eq_pp_mam_%Y%m%d_v??.cdf"
        elif instr == "pcd":
            pathformat = "pp/pcd/%Y/eq_pp_pcd_%Y%m%d_v??.cdf"
        elif instr == "sfd":
            # Only datatype='sp' is available for SFD
            pathformat = "sp/sfd/%Y/eq_sp_sfd_%Y%m%d_v??.cdf"
        else:
            logging.error("Invalid instrument type." + instr)
            continue

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
                prefix=prefix,
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
