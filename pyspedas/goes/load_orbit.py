from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load_orbit(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    prefix="",
    suffix="",
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    time_clip=True,
    force_download=False,
):
    """
    Load GOES orbit data from SPDF.

    Fetches GOES orbit data from the Space Physics Data Facility (SPDF) website:
    https://spdf.gsfc.nasa.gov/pub/data/goes/goes#/orbit/YYYY/

    Parameters
    ----------
    trange : list of str
        Time range of interest ['YYYY-MM-DD', 'YYYY-MM-DD'].
        Or, to specify more or less than a day: ['YYYY-MM-DD hh:mm:ss', 'YYYY-MM-DD hh:mm:ss'].
    probe : str or int or list of str or int
        GOES spacecraft number(s), e.g., probe=15.
    prefix : str, optional
        Prefix to add to the tplot variable names.
        By default, the added prefix is 'g[probe]_orbit_'.
    suffix : str, optional
        Suffix to add to the tplot variable names. By default, no suffix is added.
    downloadonly : bool, optional
        If True, downloads the CDF files without loading them into tplot variables. Default is False.
    notplot : bool, optional
        If True, loads the data into dictionaries containing the numpy objects instead of creating tplot variables. Default is False.
    no_update : bool, optional
        If True, only loads data from the local cache. Default is False.
    time_clip : bool, optional
        If True, clips the variables to exactly the range specified in the trange keyword. Default is False.
    force_download : bool, optional
        If True, downloads the file even if a newer version exists locally. Default is False.

    Returns
    -------
    list of str
        List of tplot variables created or list of filenames downloaded.
    """
    remote_data_dir = "https://spdf.gsfc.nasa.gov/pub/data/goes/"
    out_files = []  # list of local files downloaded
    tvars = []  # list of tplot variables created

    if not isinstance(probe, list):
        probe = [probe]

    for prb in probe:
        # yearly files
        pathformat = (
            "goes"
            + str(prb)
            + "/orbit/%Y/goes"
            + str(prb)
            + "_ephemeris_ssc_%Y0101_v??.cdf"
        )

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

        files = download(
            remote_file=remote_names,
            remote_path=remote_data_dir,
            local_path=CONFIG["local_data_dir"],
            no_download=no_update,
            force_download=force_download,
        )

        out_files_local = []

        if files is not None:
            for file in files:
                out_files_local.append(file)

        out_files.extend(out_files_local)

        tvars_local = []
        if not downloadonly:
            if prefix is None or prefix == "" or prefix == "probename":
                # Example of prefix: g15_orbit_
                prefix_local = "g" + str(prb) + "_" + "orbit_"
            else:
                prefix_local = prefix

            tvars_local = cdf_to_tplot(
                out_files_local,
                prefix=prefix_local,
                suffix=suffix,
                get_support_data=get_support_data,
                varformat=varformat,
                varnames=varnames,
                notplot=notplot,
            )
            tvars.extend(tvars_local)

            if time_clip:
                tclip(tvars_local, trange[0], trange[1], suffix="")

    if downloadonly:
        return out_files

    return tvars
