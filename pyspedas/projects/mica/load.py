import logging
import numpy as np
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot, get_data, store_data, options

from .config import CONFIG


def load(
    trange=["2019-02-01", "2019-02-02"],
    site=None,
    suffix="",
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    time_clip=False,
):
    """
    Loads data from the Magnetic Induction Coil Array (MICA)

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest with the format ['YYYY-MM-DD','YYYY-MM-DD'] or 
        to specify more or less than a day ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']. 
        Defaults to ['2019-02-01', '2019-02-02'].
    site : str, optional
        The site to load data for.
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

    Returns
    -------
    list
        List of tplot variables created.
        If downloadonly is set to True, the list of files downloaded will be returned instead.
    """

    if site is None:
        logging.error("A valid MICA site code name must be entered.")
        logging.error("Current site codes include: ")
        logging.error(
            "NAL, LYR, LOR, ISR, SDY, IQA, SNK, MCM, SPA, JBS, NEV, HAL, PG2[3,4,5]"
        )
        return

    pathformat = site.upper() + "/%Y/%m/mica_ulf_" + site.lower() + "_%Y%m%d_v??.cdf"

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(
        remote_file=remote_names,
        remote_path=CONFIG["remote_data_dir"],
        local_path=CONFIG["local_data_dir"],
        no_download=no_update,
    )
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(
        out_files,
        suffix="_" + site.upper() + suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        notplot=notplot,
    )

    # remove values > 1000; taken from IDL SPEDAS version
    for out_var in tvars:
        if out_var[0:7] == "spectra":
            times, data, freq = get_data(out_var)
            w_fill = np.where(data > 1000.0)
            data[w_fill] = np.nan
            store_data(out_var, data={"x": times, "y": data, "v": freq})
            options(out_var, "spec", True)
            options(out_var, "Colormap", "spedas")
            options(out_var, "zlog", False)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix="")

    return tvars
