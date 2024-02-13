import logging
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(
    trange=["2014-10-18", "2014-10-19"],
    instrument="mag",
    datatype="",
    level="l2",
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
    Load MAVEN data files for a given time range and instrument.

    Parameters
    ----------
    trange : list of str, optional
        Time range in the format ['start_date', 'end_date'].
        Defaults to ['2014-10-18', '2014-10-19'].
    instrument : str, optional
        Instrument name. Defaults to 'mag'.
        Valid values are: 'mag', 'swea', 'swia', 'static', 'sep', 'kp' (or 'insitu').
    datatype : str, optional
        Data type, depends on instrument.
        Valid options (default is the first value in the list):
            mag (1): 'sunstate-1sec'
            swea (5): 'arc3d', 'arcpad', 'svy3d', 'svypad', 'svyspec'
            swia (6): 'onboardsvyspec', 'onboardsvymom', 'finesvy3d', 'finearc3d', 'coarsesvy3d', 'coarsearc3d'
            static (20): 'c0-64e2m', 'c2-32e32m', 'c4-4e64m', 'c6-32e64m', 'c8-32e16d', 'ca-16e4d16a', 'cc-32e8d32m',
                'cd-32e8d32m', 'ce-16e4d16a16m', 'cf-16e4d16a16m', 'd0-32e4d16a8m', 'd1-32e4d16a8m', 'd4-4d16a2m',
                'd6-events', 'd7-fsthkp', 'd8-12r1e', 'd9-12r64e', 'da-1r64e', 'db-1024tof', 'hkp'
            sep (2): 's1-cal-svy-full', 's2-cal-svy-full'
            kp or insitu (1): 'kp-4sec'
    level : str, optional
        Data level. Defaults to 'l2'.
    suffix : str, optional
        Suffix to append to variable names. Defaults to ''.
    get_support_data : bool, optional
        Whether to retrieve support data. Defaults to False.
        By default, only data with "VAR_TYPE=data" will be loaded into tplot.
        If set to True, "VAR_TYPE=support_data" will also be loaded into tplot.
    varformat : str, optional
        Variable format. Defaults to None.
    varnames : list of str, optional
        List of variable names to load. Defaults to [].
    downloadonly : bool, optional
        Whether to only download the files without loading them into tplot. Defaults to False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables. Defaults to False.
    no_update : bool, optional
        Whether to skip updating the local data directory. Defaults to False.
    time_clip : bool, optional
        Whether to clip the loaded data to the specified time range. Defaults to False.

    Returns
    -------
    list of str
        List of loaded data variables or files downloaded.
    """
    if instrument == "mag":
        # https://spdf.gsfc.nasa.gov/pub/data/maven/mag/l2/
        # for mag, only valid options are (1): level=l2, datatype=sunstate-1sec
        pathformat = f"mag/l2/sunstate-1sec/cdfs/%Y/%m/mvn_mag_l2-sunstate-1sec_%Y%m%d_v??_r??.cdf"

    elif instrument == "swea":
        # https://spdf.gsfc.nasa.gov/pub/data/maven/swea/l2/
        # for swea, valid options are (5): level=l2, datatype=arc3d, arcpad, svy3d, svypad, svyspec
        if datatype == "":
            datatype = "arc3d"  # default
        elif datatype not in ["arc3d", "arcpad", "svy3d", "svypad", "svyspec"]:
            logging.error(
                f"Invalid datatype: {datatype}. Valid options are: arc3d, arcpad, svy3d, svypad, svyspec"
            )
            return
        pathformat = (
            f"swea/l2/{datatype}/%Y/%m/mvn_swe_l2_{datatype}_%Y%m%d_v??_r??.cdf"
        )

    elif instrument == "swia":
        # https://spdf.gsfc.nasa.gov/pub/data/maven/swia/l2/
        # for swia, valid options are (6): level=l2, datatype=onboardsvyspec, onboardsvymom, finesvy3d, finearc3d, coarsesvy3d, coarsearc3d
        if datatype == "":
            datatype = "onboardsvyspec"  # default
        elif datatype not in [
            "onboardsvyspec",
            "onboardsvymom",
            "finesvy3d",
            "finearc3d",
            "coarsesvy3d",
            "coarsearc3d",
        ]:
            logging.error(
                f"Invalid datatype: {datatype}. Valid options are: onboardsvyspec, onboardsvymom, finesvy3d, finearc3d, coarsesvy3d, coarsearc3d"
            )
            return
        pathformat = (
            f"swia/l2/{datatype}/%Y/%m/mvn_swi_l2_{datatype}_%Y%m%d_v??_r??.cdf"
        )

    elif instrument == "static":
        # https://spdf.gsfc.nasa.gov/pub/data/maven/static/l2/
        # for static, valid options are: level=l2, datatype=c0-64e2m, c2-32e32m, c4-4e64m, c6-32e64m, c8-32e16d, ca-16e4d16a,
        #    cc-32e8d32m, cd-32e8d32m, ce-16e4d16a16m, cf-16e4d16a16m, d0-32e4d16a8m, d1-32e4d16a8m, d4-4d16a2m, d6-events,
        #    d7-fsthkp, d8-12r1e, d9-12r64e, da-1r64e, db-1024tof, hkp
        static_dict = {
            "c0-64e2m": "c0-64e2m",
            "c2-32e32m": "c2-32e32m",
            "c4-4e64m": "c4-4e64m",
            "c6-32e64m": "c6-32e64m",
            "c8-32e16d": "c8-32e16d",
            "ca-16e4d16a": "ca-16e4d16a",
            "cc-32e8d32m": "cc-32e8d32m",
            "cd-32e8d32m": "cd-32e8d32m",
            "ce-16e4d16a16m": "ce-16e4d16a16m",
            "cf-16e4d16a16m": "cf-16e4d16a16m",
            "d0-32e4d16a8m": "d0-32e4d16a8m",
            "d1-32e4d16a8m": "d1-32e4d16a8m",
            "d4-4d16a2m": "d4-4d16a2m",
            "d6-events": "d6-events",
            "d7-fsthkp": "d7-fsthkp",
            "d8-12r1e": "d8-12r1e",
            "d9-12r64e": "d9-12r64e",
            "da-1r64e": "da-1r64e",
            "db-1024tof": "db-1024tof",
            "hkp": "2a-hkp",
        }
        if datatype == "":
            datatype = "c0-64e2m"  # default
        elif datatype not in static_dict.keys():
            logging.error(
                f"Invalid datatype: {datatype}. Valid options are: c0-64e2m, c2-32e32m, c4-4e64m, c6-32e64m, c8-32e16d, ca-16e4d16a, "
                "cc-32e8d32m, cd-32e8d32m, ce-16e4d16a16m, cf-16e4d16a16m, d0-32e4d16a8m, d1-32e4d16a8m, d4-4d16a2m, d6-events, "
                "d7-fsthkp, d8-12r1e, d9-12r64e, da-1r64e, db-1024tof, hkp"
            )
            return
        
        datatypefile = static_dict[datatype]
        pathformat = (
            f"static/l2/{datatype}/%Y/%m/mvn_sta_l2_{datatypefile}_%Y%m%d_v??_r??.cdf"
        )

    elif instrument == "sep":
        # https://spdf.gsfc.nasa.gov/pub/data/maven/sep/l2/
        # for sep, valid options are (2): level=l2, datatype=s1-cal-svy-full, s2-cal-svy-full
        if datatype == "":
            datatype = "s1-cal-svy-full"  # default
        elif datatype not in ["s1-cal-svy-full", "s2-cal-svy-full"]:
            logging.error(
                f"Invalid datatype: {datatype}. Valid options are: s1-cal-svy-full, s2-cal-svy-full"
            )
            return
        pathformat = f"sep/l2/{datatype}/%Y/%m/mvn_sep_l2_{datatype}_%Y%m%d_v??_r??.cdf"

    elif instrument == "kp" or instrument == "insitu":
        # https://spdf.gsfc.nasa.gov/pub/data/maven/insitu/kp-4sec/cdfs/
        # for kp, only valid options are (1): level=l2, datatype=kp-4sec
        pathformat = f"insitu/kp-4sec/cdfs/%Y/%m/mvn_insitu_kp-4sec_%Y%m%d_v??_r??.cdf"

    else:
        logging.error(
            f"Invalid instrument: {instrument}. Valid options for MAVEN SPDF downloads are: mag, swea, swia, static, sep, kp"
        )
        return

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
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        notplot=notplot,
    )

    if tvars is None or notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix="")

    return tvars
