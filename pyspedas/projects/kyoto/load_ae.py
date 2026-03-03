import logging
import re
from datetime import datetime, timedelta
from pyspedas.tplot_tools import time_clip as tclip
from pyspedas.tplot_tools import store_data, options
from pyspedas import dailynames, download
from .kyoto_config import CONFIG
from pyspedas import time_string,get_data, time_double, time_string, del_data, tnames
from pyspedas import tplot_copy
import numpy as np
import os

def ae_file_sort_keys(downloaded_files):
    keys = []
    for fn in downloaded_files:
        bn = os.path.basename(fn)  # like aeyymmdd
        yy = bn[2:4]
        mm = bn[4:6]
        dd = bn[6:8]
        if int(yy) >= 69:
            key = '19' + yy + mm + dd
        else:
            key = '20' + yy + mm + dd
        keys.append(key)
    return keys


def parse_ae_html(html_text):
    """
    Parses the HTML text and extracts date-times and values.

    Parameters
    ----------
    html_text : str
        The HTML text to be parsed.

    Returns
    -------
    tuple
        A tuple containing two lists - date_times and values.
        date_times : list
            A list of datetime objects representing the date and time.
        values : list
            A list of integers representing the AE values.
    """
    date_times = []
    values = []
    html_lines = html_text.split("\n")

    for line in html_lines:
        # AEALAOAU    100101L00AL PRVAE/E02
        match = re.match(
            r"A\w{7}\s+(\d{6})\w(\d{2})(AE|AL|AO|AU|AX)\s+\w{5,8}(?:/\w\d{2})?\s+(.*)",
            line)
        if match:
            date_str = match.group(1)
            hour_str = match.group(2)
            # Note: we are passing a 2-digit year to strptime!  Fortunately, the earliest date
            # for provisional AE data is 1996-01-01, and strptime treats any 2-digit year >= 69
            # as being in the 1900's, .so this is correct for our purposes.  JWL 2026-02-09
            date = datetime.strptime(date_str + hour_str, "%y%m%d%H")
            minute_values = match.group(4).split()
            for i, value in enumerate(minute_values):
                if i >= 60:
                    break  # the last values is the daily mean
                date_times.append(date + timedelta(minutes=i))
                values.append(int(value))
    return date_times, values


def load_ae_worker(
    trange=None,
    datatypes=["ae", "al", "ao", "au", "ax"],
    time_clip=True,
    remote_data_dir="",
    prefix="",
    suffix="",
    no_download=False,
    local_data_dir="",
    download_only=False,
    force_download=False,
    skip_realtime = False,
    skip_provisional = False
):
    """
    Downloads and loads either provisional or realtime index data (but not both) from the Kyoto World Data Center for Geomagnetism.

    Parameters
    ----------
    trange : list
        The time range of the data to download and load.
        Format: [start_time, end_time].
    datatypes : list, optional
        The types of AE index data to download and load.
        Default: ["ae", "al", "ao", "au", "ax"].
    time_clip : bool, optional
        Whether to clip the loaded data to the specified time range.
        Default: True.
    remote_data_dir : str, optional
        The remote directory where the data is located.
        Default: "https://wdc.kugi.kyoto-u.ac.jp/ae_provisional/".
    prefix : str, optional
        A prefix to add to the variable names of the loaded data.
        Default: "".
    suffix : str, optional
        A suffix to add to the variable names of the loaded data.
        Default: "".
    no_download : bool, optional
        If True, the data will not be downloaded, the local file will be used.
        Default: False.
    local_data_dir : str, optional
        The local directory where the data will be downloaded.
        Default: "".
    download_only : bool, optional
        If True, only download the data, do not load it.
        Default: False.
    force_download: bool
        Download file even if local version is more recent than server version
        Default: False
    skip_provisional: bool
        If Rrue, only attempt downloading and processing realtime data. Default: False
    skip_realtime: bool
        If True, only attempt downloading and processing provisional data. Default: False


    Returns
    -------
    list
        A list of tplot variable names created.

    """

    vars = []  # list of tplot variables created
    ack = """
            ******************************
            The provisional AE data are provided by the World Data Center for Geomagnetism, Kyoto,
            and are not for redistribution (https://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank
            AE stations (Abisko [SGU, Sweden], Cape Chelyuskin [AARI, Russia], Tixi [IKFIA and
            AARI, Russia], Pebek [AARI, Russia], Barrow, College [USGS, USA], Yellowknife,
            Fort Churchill, Sanikiluaq (Poste-de-la-Baleine) [CGS, Canada], Narsarsuaq [DMI,
            Denmark], and Leirvogur [U. Iceland, Iceland]) as well as the RapidMAG team for
            their cooperations and efforts to operate these stations and to supply data for the provisional
            AE index to the WDC, Kyoto. (Pebek is a new station at geographic latitude of 70.09N
            and longitude of 170.93E, replacing the closed station Cape Wellen.)
            ******************************
        """

    if local_data_dir == "":
        local_data_dir = CONFIG["local_data_dir"]
    if local_data_dir[-1] != "/":
        local_data_dir += "/"

    if remote_data_dir == "":
        remote_data_dir = CONFIG["remote_data_dir_ae"]

    all_datatypes = ["ae", "al", "ao", "au", "ax"]
    for i in range(len(datatypes)):
        datatype = datatypes[i].lower()
        if datatype not in all_datatypes:
            logging.error("Invalid datatype: " + datatype)
            continue  # skip to the next datatype

        rt_ff = "%Y/%m/%d/" + datatype + "%y%m%d"
        prov_ff = "%Y%m/" + datatype + "%y%m%d.for.request"

        try:
            rt_file_names = dailynames(file_format=rt_ff, trange=trange)
            prov_file_names = dailynames(file_format=prov_ff, trange=trange)
        except Exception as e:
            logging.error("Error occurred while getting file names: " + str(e))
            continue  # skip to the next datatype

        # Keep unique files names only
        rt_file_names = list(set(rt_file_names))
        prov_file_names = list(set(prov_file_names))
        # The above operation does not necessarily preserve order!  We need to sort the filenames.
        rt_file_names = sorted(rt_file_names)
        prov_file_names = sorted(prov_file_names)

        times = []
        data = []
        rt_downloaded_files = []
        prov_downloaded_files = []
        # Download the html page for each url and extract times and data
        if not skip_provisional:
            for filename in prov_file_names:
                yyyymm = ""
                if len(filename) > 6:
                    yyyymm = filename[:6]
                url = remote_data_dir + "ae_provisional/" + filename
                # Use a local path similar to IDL SPEDAS
                local_path = local_data_dir + "ae_provisional/" + datatype + "/" + yyyymm + "/"
                fname = download(url, local_path=local_path, no_download=no_download, force_download=force_download)
                if fname is not None and len(fname) >= 1:
                    prov_downloaded_files.extend(fname)

        if not skip_realtime:
            for filename in rt_file_names:
                yyyy = filename[:4]
                mm = filename[5:7]
                dd = filename[8:10]
                url = remote_data_dir + "ae_realtime/data_dir/" + filename
                # Use a local path similar to IDL SPEDAS
                local_path = local_data_dir + "ae_realtime/data_dir/" + datatype + "/" + yyyy + "/" + mm + "/" + dd + "/"

                fname = download(url, local_path=local_path, no_download=no_download, force_download=force_download)
                if fname is not None and len(fname) >= 1:
                    rt_downloaded_files.extend(fname)

        if download_only:
            continue  # skip to the next data type

        if len(rt_downloaded_files) == 0 and len(prov_downloaded_files) == 0:
            logging.warning(f"No data found in requested time range for datatype {datatype}")
            continue

        # Merge prov and realtime file lists
        # We need to use YYYYMMDD as sort/duplicate keys.  The filenames only have two digit years
        # so we need to infer (guess) the century.  Fortunately, the realtime and provisional
        # file basenames are close enough that we can use the same routine to generate sort
        # keys for both.

        rt_keys = ae_file_sort_keys(rt_downloaded_files)
        prov_keys = ae_file_sort_keys(prov_downloaded_files)

        # Check for duplicates...if found, take provisional over realtime
        rt_thinned = []
        rt_keys_thinned = []
        for k,f in zip(rt_keys, rt_downloaded_files):
            if k in prov_keys:
                logging.warning(f"Both realtime and provional {datatype} data found for date {k}, using provisional")
            else:
                rt_thinned.append(f)
                rt_keys_thinned.append(k)

        combined_keys=prov_keys + rt_keys_thinned
        combined_filenames=prov_downloaded_files + rt_thinned

        # Now sort the keys and filenames with some python zip magic
        step1=zip(combined_keys, combined_filenames)
        step2=sorted(step1)
        sorted_keys_tuple, sorted_filenames_tuple = zip(*step2)
        sorted_keys = list(sorted_keys_tuple)
        sorted_filenames = list(sorted_filenames_tuple)

        # Now iterate through the time-sorted file list, load and combine the data.

        for fname in sorted_filenames:
            try:
                with open(fname, "r") as file:
                    html_text = file.read()
                file_times, file_data = parse_ae_html(html_text)
                times.extend(file_times)
                data.extend(file_data)
            except Exception as e:
                logging.error(
                    "Error occurred while parsing " + fname + ": " + str(e)
                )
                continue  # skip to the next file

        if len(times) == 0 and not download_only:
            logging.error("No data found for " + datatype + " in the given time range.")
            continue
        if not download_only:
            # Save tplot variables
            varname = prefix + "kyoto_" + datatype + suffix
            attr = {
                "source_name": "Kyoto Provisonal",
                "instrument": datatype.upper(),
                "reference": "https://wdc.kugi.kyoto-u.ac.jp/",
                "units": "nT",
                "acknowledgement": ack,
            }
            store_data(varname, data={"x": times, "y": data}, attr_dict=attr)
            options(varname, "ytitle", "Kyoto " + datatype.upper())
            options(varname, "ysubtitle", "[nT]")

            vars.append(varname)

            if time_clip:
                tclip(varname, trange[0], trange[1], overwrite=True)

    return vars


def load_ae(
        trange=None,
        datatypes=["ae", "al", "ao", "au", "ax"],
        time_clip=True,
        remote_data_dir="",
        prefix="",
        suffix="",
        no_download=False,
        local_data_dir="",
        download_only=False,
        force_download=False,
        realtime=False,
):
    """
    Downloads and loads data from the Kyoto World Data Center for Geomagnetism.
    The realtime and provisional data sets are organized a little differently, so if necessary,
    this routine makes two calls to load_ae_worker (one for provisional, one for realtime) and
    combines the results.

    Parameters
    ----------
    trange : list
        The time range of the data to download and load.
        Format: [start_time, end_time].
    datatypes : list, optional
        The types of AE index data to download and load.
        Default: ["ae", "al", "ao", "au", "ax"].
    time_clip : bool, optional
        Whether to clip the loaded data to the specified time range.
        Default: True.
    remote_data_dir : str, optional
        The remote directory where the data is located.
        Default: "https://wdc.kugi.kyoto-u.ac.jp/ae_provisional/".
    prefix : str, optional
        A prefix to add to the variable names of the loaded data.
        Default: "".
    suffix : str, optional
        A suffix to add to the variable names of the loaded data.
        Default: "".
    no_download : bool, optional
        If True, the data will not be downloaded, the local file will be used.
        Default: False.
    local_data_dir : str, optional
        The local directory where the data will be downloaded.
        Default: "".
    download_only : bool, optional
        If True, only download the data, do not load it.
        Default: False.
    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------
    list
        A list of tplot variable names created.

    Examples
    --------
    >>> from pyspedas.projects.kyoto import load_ae
    >>> trange = ['2010-01-01 12:00:00', '2010-01-01 18:00:00']
    >>> vars = load_ae(trange=trange)
    >>> print(vars)
    ['kyoto_ae', 'kyoto_al', 'kyoto_ao', 'kyoto_au', 'kyoto_ax']
    """

    vars = []  # list of tplot variables created

    if trange is None or len(trange) != 2:
        logging.error("load_ae: Keyword trange with two datetimes is required to download data.")
        return vars
    trange_dbl = time_double(trange)
    earliest_data = time_double('1996-01-01')
    if trange_dbl[0] >= trange_dbl[1]:
        logging.error(f"load_ae: Invalid time range. End time {trange[1]} must be greater than start time {trange[0]}.")
        return vars
    if trange_dbl[1] < earliest_data:
        logging.error(f"load_ae: Invalid time range. End time {trange[1]} is earlier than 1996-01-01")
        return vars

    if local_data_dir == "":
        local_data_dir = CONFIG["local_data_dir"]
    if local_data_dir[-1] != "/":
        local_data_dir += "/"

    if remote_data_dir == "":
        remote_data_dir = CONFIG["remote_data_dir_ae"]

    ack = """
            ******************************
            The provisional AE data are provided by the World Data Center for Geomagnetism, Kyoto,
            and are not for redistribution (https://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank
            AE stations (Abisko [SGU, Sweden], Cape Chelyuskin [AARI, Russia], Tixi [IKFIA and
            AARI, Russia], Pebek [AARI, Russia], Barrow, College [USGS, USA], Yellowknife,
            Fort Churchill, Sanikiluaq (Poste-de-la-Baleine) [CGS, Canada], Narsarsuaq [DMI,
            Denmark], and Leirvogur [U. Iceland, Iceland]) as well as the RapidMAG team for
            their cooperations and efforts to operate these stations and to supply data for the provisional
            AE index to the WDC, Kyoto. (Pebek is a new station at geographic latitude of 70.09N
            and longitude of 170.93E, replacing the closed station Cape Wellen.)
            ******************************
        """
    earliest_mixed_date = "2024-05-10/00:00:00"
    latest_mixed_date = "2024-05-15/00:00:00"
    latest_provisional_only = "2021-01-01/00:00:00"
    skip_realtime = False
    skip_provisional = False
    if time_double(trange[1]) <= time_double(latest_provisional_only):
        skip_realtime = True
    elif time_double(trange[0]) >= time_double(latest_mixed_date):
        skip_provisional = True

    retvalue = load_ae_worker(trange=trange,
                              datatypes=datatypes,
                              time_clip=time_clip,
                              remote_data_dir=remote_data_dir,
                              prefix=prefix,
                              suffix=suffix,
                              no_download=no_download,
                              local_data_dir=local_data_dir,
                              force_download=force_download,
                              skip_realtime=skip_realtime,
                              skip_provisional=skip_provisional,
                              )
    # Print the acknowledgments
    logging.info(ack)
    return retvalue
