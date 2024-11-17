from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import netcdf_to_tplot

from .config import CONFIG


def loadr(
    trange=["2023-01-01", "2023-01-02 11:59:59"],
    probe="18",
    instrument="mag",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=True,
    force_download=False,
):
    """
    Loads GOES-R L2 data (GOES-16 and later) for specified instruments and data types.

    Parameters
    ----------
    trange : list of str
        Time range of interest [starttime, endtime].
    probe : str or int or list of str or int
        GOES spacecraft number(s), e.g., probe=16 or probe=[16, 17].
    instrument : str or list of str
        Name of the instrument (e.g., 'euvs', 'xrs', 'mag', 'mpsh', 'sgps').
    datatype : str, optional
        Data resolution, default is '1min'. Valid options: 'low' (avg), 'hi' (full), among others depending on the instrument.
    prefix : str, optional
        Prefix to add to the tplot variable names. Defaults to an empty string.
    suffix : str, optional
        Suffix to add to the tplot variable names. Defaults to an empty string.
    downloadonly : bool, optional
        If True, downloads the CDF files without loading them into tplot variables. Default is False.
    no_update : bool, optional
        If True, only loads data from the local cache. Default is False.
    time_clip : bool, optional
        If True (the default), clips the variables to exactly the range specified in the trange keyword.
    force_download : bool, optional
        If True, downloads the file even if a newer version exists locally. Default is False.

    Returns
    -------
    list
        List of tplot variables created or list of filenames downloaded.

    Notes
    -----
    - Information can be found at https://www.ngdc.noaa.gov/stp/satellite/goes-r.html.
    - Data is available at https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/.
    - Path format: goesNN/l2/data/instrument/YYYY/MM/file.nc.
    - Time variable is 'time', seconds since 2000-01-01 12:00:00.
    - GOES-EAST (GOES-16, 2017-), GOES-WEST (GOES-17, 2018-2022; GOES-18, 2023-).

    Examples
    --------
    >>> from pyspedas.projects.goes import load
    >>> trange = ['2023-01-01', '2023-01-02']
    >>> vars = load(trange=trange, probe='16', instrument='mag', datatype='1min', time_clip=True)
    >>> print(vars)
    ['g16_mag_DQF', 'g16_mag_b_brf', 'g16_mag_b_eci', 'g16_mag_b_epn', 'g16_mag_b_gse',
    'g16_mag_b_gsm', 'g16_mag_b_quality', 'g16_mag_b_total', 'g16_mag_b_vdh',
    'g16_mag_num_points', 'g16_mag_orbit_llr_geo']
    """

    goes_path_dir = (
        "https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/"
    )
    time_var = "time"  # name of the time variable in the netcdf files
    out_files = []
    tvars = []

    if isinstance(probe, tuple):
        probe = list(probe)
    if not isinstance(probe, list):
        probe = [probe]
    probe = [str(p) for p in probe]
    if not isinstance(instrument, list):
        instrument = [instrument]

    for prb in probe:
        remote_path = "goes" + str(prb) + "/l2/data/"
        pathformat = []

        for instr in instrument:
            if instr == "euvs":
                if datatype in ["full", "hi", "1min", "avg1m"]:  # high resolution 1 min
                    pathformat = [
                        remote_path
                        + "euvs-l2-avg1m_science/%Y/%m/sci_euvs-l2-avg1m_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
                else:  # low resolution 1 day, smaller files
                    pathformat = [
                        remote_path
                        + "euvs-l2-avg1d_science/%Y/%m/sci_euvs-l2-avg1d_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
            elif instr == "xrs":
                if datatype in ["full", "hi", "1sec", "flx1s"]:  # high resolution 1 sec
                    pathformat = [
                        remote_path
                        + "xrsf-l2-flx1s_science/%Y/%m/sci_xrsf-l2-flx1s_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
                else:  # low resolution 1 min, smaller files
                    pathformat = [
                        remote_path
                        + "xrsf-l2-avg1m_science/%Y/%m/sci_xrsf-l2-avg1m_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
            elif instr == "mag":
                if datatype in [
                    "full",
                    "hi",
                    "0.1sec",
                    "hires",
                ]:  # high resolution 0.1 sec
                    pathformat = [
                        remote_path
                        + "magn-l2-hires/%Y/%m/dn_magn-l2-hires_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
                else:  # low resolution 1 min, smaller files
                    pathformat = [
                        remote_path
                        + "magn-l2-avg1m/%Y/%m/dn_magn-l2-avg1m_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
            elif instr == "mpsh":
                time_var = "L2_SciData_TimeStamp"
                if datatype in [
                    "full",
                    "hi",
                    "1min",
                    "avg1m",
                    "1m",
                ]:  # high resolution 1 min
                    pathformat = [
                        remote_path
                        + "mpsh-l2-avg1m/%Y/%m/sci_mpsh-l2-avg1m_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
                else:  # low resolution 5 min, smaller files
                    pathformat = [
                        remote_path
                        + "mpsh-l2-avg5m/%Y/%m/sci_mpsh-l2-avg5m_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
            elif instr == "sgps":
                if datatype in [
                    "full",
                    "hi",
                    "1min",
                    "avg1m",
                    "1m",
                ]:  # high resolution 1 min
                    pathformat = [
                        remote_path
                        + "sgps-l2-avg1m/%Y/%m/sci_sgps-l2-avg1m_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]
                else:  # low resolution 5 min, smaller files
                    pathformat = [
                        remote_path
                        + "sgps-l2-avg5m/%Y/%m/sci_sgps-l2-avg5m_g"
                        + str(prb)
                        + "_d%Y%m%d_v?-?-?.nc"
                    ]

            # find the full remote path names using the trange
            if not isinstance(pathformat, list):
                pathformat = [pathformat]

            remote_names = []
            for path in pathformat:
                remote_names.extend(dailynames(file_format=path, trange=trange))

            # For each probe and instrument, download the files
            files = download(
                remote_file=remote_names,
                remote_path=goes_path_dir,
                local_path=CONFIG["local_data_dir"],
                no_download=no_update,
                force_download=force_download,
            )

            files = sorted(set(files))
            out_files.extend(files)

            if len(files) > 0 and not downloadonly:
                if prefix is None or prefix == "" or prefix == "probename":
                    # Example of prefix: g16_xrs_
                    prefix_local = "g" + str(prb) + "_" + instr + "_"
                else:
                    prefix_local = prefix

                # Load all files from the same probe and instrument, merging them
                tvars_local = netcdf_to_tplot(
                    files, prefix=prefix_local, suffix=suffix, time=time_var
                )
                if len(tvars_local) > 0:
                    tvars.extend(tvars_local)
                    if time_clip:
                        tclip(tvars_local, trange[0], trange[1], overwrite=True)

    if downloadonly:
        return out_files

    tvars = sorted(set(tvars))
    return tvars


def load(
    trange=["2013-11-05", "2013-11-06 12:00:00"],
    probe="15",
    instrument="fgm",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=True,
    force_download=False,
):
    """
    Load GOES L2 data.

    Parameters
    ----------
    trange : list of str
        Time range of interest ['YYYY-MM-DD', 'YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss', 'YYYY-MM-DD/hh:mm:ss'].
    probe : str, int, or list of str/int
        GOES spacecraft number(s), e.g., probe=15.
    instrument : str or list of str
        Name of the instrument. For GOES 8-15: 'fgm', 'eps', 'epead', 'maged', 'magpd', 'hepad', 'xrs'.
        For GOES-R 16-18: 'euvs', 'xrs', 'mag', 'mpsh', 'sgps'.
    datatype : str
        Data type; usually instrument resolution, depends on the instrument (default '1min').
        Valid for GOES 8-15: 'hi', 'low', 'full', 'avg', '1min', '5min'.
        Valid for GOES-R 16-18: 'hi', 'low', 'full', 'avg', and other options.
    prefix : str, optional
        Prefix to add to the tplot variable names. By default, no prefix is added.
        If prefix is 'probename', then the name will be used, for example, 'g16'.
    suffix : str, optional
        Suffix to add to the tplot variable names. By default, no suffix is added.
    downloadonly : bool, optional
        If True, downloads the CDF files without loading them into tplot variables. Default is False.
    no_update : bool, optional
        If True, only loads data from the local cache. Default is False.
    time_clip : bool, optional
        If True (the default), clips the variables to exactly the range specified in the trange keyword.
    force_download : bool, optional
        If True, downloads the file even if a newer version exists locally. Default is False.

    Returns
    -------
    list of str
        List of tplot variables created or list of filenames downloaded.

    Examples
    --------
    >>> from pyspedas.projects.goes import load
    >>> trange = ['2019-01-01', '2019-01-02']
    >>> vars = load(trange=trange, probe='15', instrument='fgm', datatype='1min', time_clip=True)
    >>> print(vars)
    ['g15_fgm_BX_1_QUAL_FLAG', 'g15_fgm_BX_1_NUM_PTS', 'g15_fgm_BX_1', ...]
    (the result is a list of 66 variables)
    """

    if isinstance(probe, tuple):
        probe = list(probe)
    if not isinstance(probe, list):
        probe = [probe]
    probe = [str(p) for p in probe]
    if not isinstance(instrument, list):
        instrument = [instrument]

    probe_r = []  # GOES-R probes
    probe_s = []  # GOES probes
    out_files_r = []  # GOES-R files to download
    out_files = []  # GOES files to download
    tvars_r = []  # GOES-R list of variables created
    tvars = []  # all variables created

    # Find if we need to call the GOES-R load function for some probes
    for prb in probe:
        if int(prb) > 15:
            probe_r.append(str(prb))
        else:
            probe_s.append(str(prb))

    if len(probe_r):
        tvars_r = loadr(
            trange=trange,
            probe=probe_r,
            instrument=instrument,
            datatype=datatype,
            prefix=prefix,
            suffix=suffix,
            downloadonly=downloadonly,
            no_update=no_update,
            time_clip=time_clip,
            force_download=force_download,
        )
        if downloadonly:
            out_files_r = tvars_r

    # Continue with loading GOES (1-15) data
    for prb in probe_s:
        avg_path = "avg/%Y/%m/goes" + str(prb) + "/netcdf/" + "g" + str(prb)
        full_path = "full/%Y/%m/goes" + str(prb) + "/netcdf/" + "g" + str(prb)

        for instr in instrument:
            pathformat = []
            if instr == "fgm":
                if datatype == "512ms" or datatype == "full":  # full, unaveraged data
                    pathformat = full_path + "_magneto_512ms_%Y%m%d_%Y%m%d.nc"
                elif datatype == "5min":  # 5 min averages
                    pathformat = avg_path + "_magneto_5m_%Y%m01_%Y%m??.nc"
                else:  # 1 min averages, goes13, goes15 only contain 1m averages
                    pathformat = avg_path + "_magneto_1m_%Y%m01_%Y%m??.nc"
            elif instr == "eps":
                # energetic particle sensor -- only valid for GOES-08 through GOES-12, only averaged data available
                if datatype == "1min" or datatype == "full":
                    pathformat = avg_path + "_eps_1m_%Y%m01_%Y%m??.nc"
                else:  # 'low' or 5min
                    pathformat = avg_path + "_eps_5m_%Y%m01_%Y%m??.nc"
            elif instr == "epead":
                # electron, proton, alpha detector -- only valid on GOES-13, 14, 15
                if datatype == "1min":
                    pathformat = [
                        "_epead_e13ew_1m_%Y%m01_%Y%m??.nc",
                        "_epead_p17ew_1m_%Y%m01_%Y%m??.nc",
                        "_epead_a16ew_1m_%Y%m01_%Y%m??.nc",
                    ]
                    pathformat = [avg_path + s for s in pathformat]
                elif datatype == "5min" or datatype == "low":
                    pathformat = [
                        "_epead_e13ew_5m_%Y%m01_%Y%m??.nc",
                        "_epead_p17ew_5m_%Y%m01_%Y%m??.nc",
                        "_epead_a16ew_5m_%Y%m01_%Y%m??.nc",
                    ]
                    pathformat = [avg_path + s for s in pathformat]
                else:  # full
                    pathformat = [
                        "_epead_a16e_32s_%Y%m%d_%Y%m%d.nc",
                        "_epead_a16w_32s_%Y%m%d_%Y%m%d.nc",
                        "_epead_e1ew_4s_%Y%m%d_%Y%m%d.nc",
                        "_epead_e2ew_16s_%Y%m%d_%Y%m%d.nc",
                        "_epead_e3ew_16s_%Y%m%d_%Y%m%d.nc",
                        "_epead_p1ew_8s_%Y%m%d_%Y%m%d.nc",
                        "_epead_p27e_32s_%Y%m%d_%Y%m%d.nc",
                        "_epead_p27w_32s_%Y%m%d_%Y%m%d.nc",
                    ]
                    pathformat = [full_path + s for s in pathformat]
            elif instr == "maged":
                # magnetospheric electron detector -- only valid on GOES 13, 14, 15
                if datatype == "1min":
                    pathformat = avg_path + "_maged_19me15_1m_%Y%m01_%Y%m??.nc"
                elif datatype == "5min" or datatype == "low":
                    pathformat = avg_path + "_maged_19me15_5m_%Y%m01_%Y%m??.nc"
                else:  # full
                    channels = ["me1", "me2", "me3", "me4", "me5"]
                    resolution = ["2", "2", "4", "16", "32"]
                    pathformat = []
                    for idx, channel in enumerate(channels):
                        pathformat.append(
                            "_maged_19"
                            + channel
                            + "_"
                            + resolution[idx]
                            + "s_%Y%m%d_%Y%m%d.nc"
                        )
                    pathformat = [full_path + s for s in pathformat]
            elif instr == "magpd":
                # magnetospheric proton detector -- only valid on GOES 13, 14, 15
                if datatype == "1min" or datatype == "low":
                    pathformat = avg_path + "_magpd_19mp15_1m_%Y%m01_%Y%m??.nc"
                else:  # full
                    channels = ["mp1", "mp2", "mp3", "mp4", "mp5"]
                    resolution = ["16", "16", "16", "32", "32"]
                    pathformat = []
                    for idx, channel in enumerate(channels):
                        pathformat.append(
                            "_magpd_19"
                            + channel
                            + "_"
                            + resolution[idx]
                            + "s_%Y%m%d_%Y%m%d.nc"
                        )
                    pathformat = [full_path + s for s in pathformat]
            elif instr == "hepad":
                # high energy proton and alpha detector -- valid for GOES 08-15
                if datatype == "1min":
                    pathformat = [
                        "_hepad_ap_1m_%Y%m01_%Y%m??.nc",
                        "_hepad_s15_1m_%Y%m01_%Y%m??.nc",
                    ]
                    pathformat = [avg_path + s for s in pathformat]
                elif datatype == "5min" or datatype == "low":
                    pathformat = [
                        "_hepad_ap_5m_%Y%m01_%Y%m??.nc",
                        "_hepad_s15_5m_%Y%m01_%Y%m??.nc",
                    ]
                    pathformat = [avg_path + s for s in pathformat]
                else:
                    pathformat = [
                        "_hepad_ap_32s_%Y%m%d_%Y%m%d.nc",
                        "_hepad_s15_4s_%Y%m%d_%Y%m%d.nc",
                    ]
                    pathformat = [full_path + s for s in pathformat]
            elif instr == "xrs":
                # x-ray sensor -- valid for GOES 08-15
                if datatype == "1min":
                    pathformat = avg_path + "_xrs_1m_%Y%m01_%Y%m??.nc"
                elif datatype == "5min" or datatype == "low":
                    pathformat = avg_path + "_xrs_5m_%Y%m01_%Y%m??.nc"
                else:
                    pathformat = [
                        "_xrs_2s_%Y%m%d_%Y%m%d.nc",
                        "_xrs_3s_%Y%m%d_%Y%m%d.nc",
                    ]
                    pathformat = [full_path + s for s in pathformat]

            # find the full remote path names using the trange
            if not isinstance(pathformat, list):
                pathformat = [pathformat]

            remote_names = []
            for path in pathformat:
                remote_names.extend(dailynames(file_format=path, trange=trange))

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

            tvars_local = []
            if len(files) > 0 and downloadonly is False:
                if prefix is None or prefix == "" or prefix == "probename":
                    # Example of prefix: g15_xrs_
                    prefix_local = "g" + str(prb) + "_" + instr + "_"
                else:
                    prefix_local = prefix

                tvars_local = netcdf_to_tplot(
                    files, prefix=prefix_local, suffix=suffix, time="time_tag"
                )

                if len(tvars_local) > 0:
                    tvars.extend(tvars_local)
                    if time_clip:
                        tclip(
                            tvars_local, trange[0], trange[1], suffix="", overwrite=True
                        )

    if downloadonly:
        out_files.extend(out_files_r)  # append GOES-R filenames
        out_files = sorted(set(out_files))
        return out_files

    if len(tvars_r):
        tvars.extend(tvars_r)  # append GOES-R variables

    return tvars
