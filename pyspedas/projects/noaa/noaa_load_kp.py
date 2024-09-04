"""
Loads geomagnetic index data into tplot variables.

Data is downloaded from the NOAA or GFZ (Helmholtz Centre Potsdam) ftp sites.

Data is stored in tplot variables with the following names:

["Kp", "ap", "Sol_Rot_Num", "Sol_Rot_Day", "Kp_Sum", "ap_Mean", "Cp", "C9", "Sunspot_Number", "F10.7", "Flux_Qualifier"]
"""

import logging, os
import numpy as np
from pytplot import (
    time_string,
    time_double,
    store_data,
    options,
    time_clip as tclip,
)
from pyspedas.projects.noaa.config import CONFIG
from pyspedas.utilities.download_ftp import download_ftp
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download


def kp_return_fraction(value):
    """
    Calculate the fractional part of the Kp index.

    Parameters
    ----------
    value : int
        The Kp value in integer format.

    Returns
    -------
    list of float
        The fractional part of the Kp index.
    """
    value = np.array(value, dtype=np.float64)
    kp_lhs = value // 10
    kp_rhs_times_3 = value % 10
    kp_rhs = kp_rhs_times_3 // 3.0
    return kp_lhs + kp_rhs / 3.0


def convert_to_float_or_int(a, outtype="int"):
    """
    Converts a list of strings to either float or int.

    Parameters
    ----------
    a : list of str
        The list of values to be converted.
    outtype : str
        The desired output type, "float" or "int". Default is "int".

    Returns
    -------
    list of int or float:
        The converted list of values.
    """
    ans = []
    for v in a:
        try:
            if outtype == "float":
                ans.append(float(v))
            else:  # outtype == "int"
                ans.append(int(v))
        except ValueError:
            ans.append(0)
    return ans


def load_kp_to_tplot(
    trange=[0, 0],
    files=[],
    datatype=[],
    prefix="",
    suffix="",
):
    """
    Load Kp index data into tplot variables.

    These are text files that have to be parsed to extract the data and store it in tplot variables.

    Parameters
    ----------
    trange : list of str
        Time range to load data for. Should be a list of two strings.
    datatype : list of str, optional
        Type of index to load. Default is an empty list, which loads all available data.

    Returns
    -------
    list of str
        List of tplot variables that contain the data.
    """
    vars = []

    if files is None or len(files) == 0:
        logging.error("No files specified")
        return vars
    elif not isinstance(files, list):
        files = [files]

    if datatype is None or datatype == [] or len(datatype) == 0:
        datatype = [
            "Kp",
            "ap",
            "Sol_Rot_Num",
            "Sol_Rot_Day",
            "Kp_Sum",
            "ap_Mean",
            "Cp",
            "C9",
            "Sunspot_Number",
            "F10.7",
            "Flux_Qualifier",
        ]
    elif not isinstance(datatype, list):
        datatype = [datatype]
    datatype = [d.lower() for d in datatype]

    # Each line in the files contains data for one day.
    # The first 3 quantities are measured every 3 hours (8 measurements per day).
    kpdata = []
    apdata = []
    kptimes = []

    daytimes = []
    srndata = []
    srddata = []
    kpsdata = []
    apmdata = []
    cpdata = []
    c9data = []
    ssndata = []
    srfdata = []
    fqdata = []

    for kpfile in files:
        # Example line contained in these files:
        # 1701012502 73337272323302017210 18 22 12  9  9 15  7  6 120.73---070.10
        # Line length is 73 for NOAA files and 63 for WDC files (both counts include \n).

        with open(kpfile, "r") as f:
            for line in f:
                if len(line) < 63 or line.startswith("#") or line.startswith(" "):
                    # Skip lines that are less than 63 characters long (62 data and \n)
                    continue

                # Get datetimes (0:6 characters)
                year = line[0:2]
                if "00" <= year <= "69":
                    year = "20" + year
                else:
                    year = "19" + year
                month = line[2:4]
                day = line[4:6]
                ymd = year + "-" + month + "-" + day
                daytimes.append(time_double(ymd))
                for k in range(8):
                    dd = time_double(ymd + " " + "{:02d}".format(k * 3) + ":00:00")
                    kptimes.append(dd)

                # Get data (6:71 characters)
                srndata.append(line[6:10])
                srddata.append(line[10:12])
                for k in range(8):
                    kpdata.append(line[12 + 2 * k : 14 + 2 * k])
                kpsdata.append(line[28:31])
                for k in range(8):
                    apdata.append(line[31 + 3 * k : 34 + 3 * k])
                apmdata.append(line[55:58])
                cpdata.append(line[58:61])
                c9data.append(line[61:62])
                if len(line) >= 72:
                    ssndata.append(line[62:65])
                    srfdata.append(line[65:70])
                    fqdata.append(line[70:71])

    # At this point, list are strings. Convert to numbers.
    srndata = convert_to_float_or_int(srndata)
    srddata = convert_to_float_or_int(srddata)
    kpdata = convert_to_float_or_int(kpdata)
    kpsdata = convert_to_float_or_int(kpsdata)
    apdata = convert_to_float_or_int(apdata)
    apmdata = convert_to_float_or_int(apmdata)
    cpdata = convert_to_float_or_int(cpdata, "float")
    c9data = convert_to_float_or_int(c9data)
    ssndata = convert_to_float_or_int(ssndata)
    srfdata = convert_to_float_or_int(srfdata, "float")
    fqdata = convert_to_float_or_int(fqdata)

    # Check for empty data set. If empty, return.
    if len(kptimes) == 0:
        logging.error("No data found.")
        return vars
    if (
        len(trange) == 2
        and trange[0] != 0
        and time_double(trange[1]) > time_double(trange[0])
        and (
            time_double(trange[1]) < kptimes[0] or time_double(trange[0]) > kptimes[-1]
        )
    ):
        logging.error("No data found in time range.")
        return vars

    # Store tplot variables
    # kp (3-hour Kp)
    if "kp" in datatype:
        vn = prefix + "Kp" + suffix
        store_data(vn, data={"x": kptimes, "y": kp_return_fraction(kpdata)})
        options(vn, "ytitle", "Kp")
        vars.append(vn)
    # ap (3-hour ap)
    if "ap" in datatype:
        vn = prefix + "ap" + suffix
        store_data(vn, data={"x": kptimes, "y": apdata})
        options(vn, "ytitle", "ap")
        vars.append(vn)
    # sol_rot_num (solar rotation number)
    if "sol_rot_num" in datatype:
        vn = prefix + "Sol_Rot_Num" + suffix
        store_data(vn, data={"x": daytimes, "y": srndata})
        options(vn, "ytitle", "Sol_Rot_Num")
        vars.append(vn)
    # sol_rot_day (day of solar rotation)
    if "sol_rot_day" in datatype:
        vn = prefix + "Sol_Rot_Day" + suffix
        store_data(vn, data={"x": daytimes, "y": srddata})
        options(vn, "ytitle", "Sol_Rot_Day")
        vars.append(vn)
    # kp_sum (sum of Kp)
    if "kp_sum" in datatype:
        vn = prefix + "Kp_Sum" + suffix
        store_data(vn, data={"x": daytimes, "y": kpsdata})
        options(vn, "ytitle", "Kp_Sum")
        vars.append(vn)
    # ap_mean (mean of Ap)
    if "ap_mean" in datatype:
        vn = prefix + "ap_Mean" + suffix
        store_data(vn, data={"x": daytimes, "y": apmdata})
        options(vn, "ytitle", "ap_Mean")
        vars.append(vn)
    # cp (planetary C index)
    if "cp" in datatype:
        vn = prefix + "Cp" + suffix
        store_data(vn, data={"x": daytimes, "y": cpdata})
        options(vn, "ytitle", "Cp")
        vars.append(vn)
    # c9 (9-point C index)
    if "c9" in datatype:
        vn = prefix + "C9" + suffix
        store_data(vn, data={"x": daytimes, "y": c9data})
        options(vn, "ytitle", "C9")
        vars.append(vn)

    # The following do not exist in the GFZ data
    # sunspot_number (sunspot number)
    lentimes = len(daytimes)
    if "sunspot_number" in datatype and len(ssndata) > 0 and len(ssndata) == lentimes:
        vn = prefix + "Sunspot_Number" + suffix
        store_data(vn, data={"x": daytimes, "y": ssndata})
        options(vn, "ytitle", "Sunspot_Number")
        vars.append(vn)
    # f10.7 (10.7 cm solar radio flux)
    if "f10.7" in datatype and len(srfdata) > 0 and len(srfdata) == lentimes:
        vn = prefix + "F10.7" + suffix
        store_data(vn, data={"x": daytimes, "y": srfdata})
        options(vn, "ytitle", "F10.7")
        vars.append(vn)
    # flux_qualifier (10.7 cm solar radio flux qualifier)
    if "flux_qualifier" in datatype and len(fqdata) > 0 and len(fqdata) == lentimes:
        vn = prefix + "Flux_Qualifier" + suffix
        store_data(vn, data={"x": daytimes, "y": fqdata})
        options(vn, "ytitle", "Flux_Qualifier")
        vars.append(vn)

    return vars


def noaa_load_kp(
    trange=["2017-03-01/00:00:00", "2017-03-31/23:59:59"],
    kp_mirror=None,
    remote_kp_dir=None,
    local_kp_dir=None,
    datatype=[],
    gfz=False,
    gfz_ftp=False,
    prefix="",
    suffix="",
    time_clip=True,
    force_download=False,
):
    """
    Load geomagnetic index data into appropriate variables.


    Parameters
    ----------
    trange : list of str
        Time range to load data for. Should be a list of two strings.
    kp_mirror : str
        HTTP server where mirrored Kp/Ap data resides.
    remote_kp_dir : str
        Directory where the Kp/Ap data lives on the mirror server.
    local_kp_dir : str
        Directory where data is saved locally.
    datatype : list of str, optional
        Type of index to load. Default is an empty list, which loads all available data. Valid values:
            "Kp",
            "ap",
            "Sol_Rot_Num",
            "Sol_Rot_Day",
            "Kp_Sum",
            "ap_Mean",
            "Cp",
            "C9",
            "Sunspot_Number",
            "F10.7",
            "Flux_Qualifier",
    gfz : bool, optional
        Load data from the HTTPS site of the German Research Centre for Geosciences, instead of NOAA.
        This is the default behavior if the end time is on or after 2018.
        Default is False (by default, it loads data from the ftp server of NOAA).
        If this source is used, the Sunspot_Number, F10.7, and Flux_Qualifier datatypes will not be available.
    gfz_ftp : bool, optional
        Load data from the ftp site of GFZ instead of https site. This is legacy behavior.
        Default is False.
    prefix: str, optional
        If provided, specifies a string to be prepended to tplot variable names.
    suffix: str, optional
        If provided, specifies a string to be appended to tplot variable names.
    time_clip: bool, optional
        If True, data will be time clipped to the exact time range requested.
        Default is True.
    force_download: bool
        Download file even if local version is more recent than server version.
        Default is False.

    Returns
    -------
    list of str
        Returns the names of tplot variables that contain all the data.
        Data is saved in a tplot variables.

    Example
    -------
    >>> from pyspedas import noaa_load_kp
    >>> vars = noaa_load_kp(trange=['2014-03-23/00:00:00', '2014-03-23/23:59:59'])
    >>> print(vars)
    ['Kp', 'ap', 'Sol_Rot_Num', 'Sol_Rot_Day', 'Kp_Sum', 'ap_Mean', 'Cp', 'C9', 'Sunspot_Number', 'F10.7', 'Flux_Qualifier']

    """
    vars = []

    if len(trange) == 2:
        trangestr = time_string(time_double(trange))
        start_year = int(trangestr[0][0:4])
        end_year = int(trangestr[1][0:4])
    else:
        logging.error("Invalid time range")
        return
    if end_year > start_year + 3:  # Limit to 4 years
        end_year = start_year + 3
        trange[1] = str(end_year) + "-12-31/00:00:00"
        logging.warning(
            "Time limit is 4 years, new time range is " + trange[0] + " to " + trange[1]
        )
    elif end_year < start_year:
        end_year = start_year
        trange[1] = str(end_year) + "-12-31/00:00:00"
        logging.warning(
            "End time is before start time, new time range is "
            + trange[0]
            + " to "
            + trange[1]
        )

    # Remote site and directory
    use_ftp = True
    if gfz or end_year >= 2018:
        if gfz_ftp:
            kp_mirror = "ftp.gfz-potsdam.de"
            remote_kp_dir = "/pub/home/obs/kp-ap/wdc/yearly/"
            gfz = True
            pre = "kp"
            suf = ".wdc"
            use_ftp = True
        else:
            use_ftp = False
    else:
        kp_mirror = kp_mirror or "ftp.ngdc.noaa.gov"
        remote_kp_dir = remote_kp_dir or "/STP/GEOMAGNETIC_DATA/INDICES/KP_AP/"
        pre = ""
        suf = ""
        use_ftp = True

    # Local directory
    if not local_kp_dir:
        local_data_dir = CONFIG["local_data_dir"]
    else:
        local_data_dir = local_kp_dir

    if len(local_data_dir) > 0 and not local_data_dir.endswith(os.sep):
        local_data_dir += os.sep

    if use_ftp:
        logging.info("Loading geomagnetic index data from " + kp_mirror + remote_kp_dir)
        # Remote names
        remote_names = [
            pre + str(year) + suf for year in range(start_year, end_year + 1)
        ]

        files = []
        # In this case, filesnames are just the year (2020, 2021, etc.)
        for yearstr in remote_names:
            dfile = download_ftp(
                kp_mirror,
                remote_kp_dir,
                yearstr,
                local_data_dir,
                force_download=force_download,
            )
            if len(dfile) > 0:
                files.append(dfile[0])
    else:
        # use https for gfz data
        gfz_path_http = (
            "https://datapub.gfz-potsdam.de/download/10.5880.Kp.0001/Kp_definitive/"
        )
        logging.info("Loading geomagnetic index data from " + gfz_path_http)
        pathformat = "Kp_def%Y.wdc"
        remote_names = dailynames(file_format=pathformat, trange=trange)
        files = download(
            remote_file=remote_names,
            remote_path=gfz_path_http,
            local_path=local_data_dir,
            force_download=force_download,
        )

    if len(files) == 0:
        logging.error("No files found.")
        return vars

    vars = load_kp_to_tplot(
        trange=trange,
        files=list(set(files)),
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
    )

    if time_clip:
        tclip(vars, trange[0], trange[1], overwrite=True)

    return vars
