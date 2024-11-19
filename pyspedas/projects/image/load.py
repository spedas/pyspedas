from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(
    trange=["2004-11-5", "2004-11-6"],
    instrument="lena",
    datatype="k0",
    suffix='',
    prefix='',
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
    Load IMAGE data.

    This function loads data from the Image mission; this function is not meant
    to be called directly; instead, see the wrappers:
    pyspedas.projects.image.lena
    pyspedas.projects.image.mena
    pyspedas.projects.image.hena
    pyspedas.projects.image.rpi
    pyspedas.projects.image.euv
    pyspedas.projects.image.fuv
    pyspedas.projects.image.orbit


    Parameters
    ----------
    trange : list of str, optional
        Time range for the data in the format ['start_date', 'end_date'].
        Defaults to ['2004-11-5', '2004-11-6'].
    instrument : str, optional
        Instrument name. Defaults to 'lena'.
    datatype : str, optional
        Data type. Defaults to 'k0'.
    suffix : str, optional
        Suffix to be added to the variable names. Defaults to ''.
    prefix: str, optional
        Prefix to be added to the variable names. Defaults to ''.
    get_support_data : bool, optional
        Flag indicating whether to retrieve support data. Defaults to False.
    varformat : str, optional
        Variable format. Defaults to None.
    varnames : list of str, optional
        List of variable names to load. Defaults to [].
    downloadonly : bool, optional
        Flag indicating whether to only download the files without loading the data. Defaults to False.
    notplot : bool, optional
        Flag indicating whether to return the loaded data without plotting. Defaults to False.
    no_update : bool, optional
        Flag indicating whether to skip updating the data files. Defaults to False.
    time_clip : bool, optional
        Flag indicating whether to clip the loaded data to the specified time range. Defaults to False.
    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------
    list or dict
        If `downloadonly` is True, returns a list of downloaded file names.
        If `notplot` is True, returns a dictionary of loaded data variables.
        Otherwise, returns a list of loaded data variables.
    """

    if instrument == "lena":
        pathformat = (
            instrument
            + "/"
            + instrument
            + "_"
            + datatype
            + "/%Y/im_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "mena":
        pathformat = (
            instrument
            + "/"
            + instrument
            + "_"
            + datatype
            + "/%Y/im_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "hena":
        pathformat = (
            instrument
            + "/"
            + instrument
            + "_"
            + datatype
            + "/%Y/im_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "rpi":
        pathformat = (
            instrument
            + "/"
            + instrument
            + "_"
            + datatype
            + "/%Y/im_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "euv":
        pathformat = (
            instrument
            + "/"
            + instrument
            + "_"
            + datatype
            + "/%Y/im_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "fuv":
        pathformat = (
            instrument
            + "/wic_"
            + datatype
            + "/%Y/im_"
            + datatype
            + "_wic_%Y%m%d_v??.cdf"
        )
    elif instrument == "orbit":
        if datatype == "def_or":
            pathformat = instrument + "/def_or/%Y/im_or_def_%Y%m%d_v??.cdf"
        elif datatype == "pre_or":
            pathformat = instrument + "/pre_or/%Y/im_or_pre_%Y%m%d_v??.cdf"

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(
        remote_file=remote_names,
        remote_path=CONFIG["remote_data_dir"],
        local_path=CONFIG["local_data_dir"],
        no_download=no_update,
        force_download=force_download,
    )
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(
        out_files,
        suffix=suffix,
        prefix=prefix,
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
