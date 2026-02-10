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

def merge_provisional_realtime(prov_list, realtime_list):
    return_list = []
    for datatype in ['ae', 'al', 'ao', 'au', 'ax']:
        prov_tmpname = "kyoto_ae_tmp_prov_kyoto_" + datatype
        realtime_tmpname = "kyoto_ae_tmp_realtime_kyoto_" + datatype
        return_name = 'kyoto_' + datatype
        if (prov_tmpname in prov_list) and (realtime_tmpname not in realtime_list):
            # provisional data. but no realtime
            tplot_copy(prov_tmpname, return_name)
            return_list.append(return_name)
        elif (prov_tmpname not in prov_list) and (realtime_tmpname in realtime_list):
            # realtime data, but no provisional
            tplot_copy(realtime_tmpname, return_name)
            return_list.append(return_name)
        elif (prov_tmpname in prov_list) and (realtime_tmpname in realtime_list):
            prov_data = get_data(prov_tmpname)
            prov_md = get_data(prov_tmpname, metadata=True)
            realtime_data = get_data(realtime_tmpname)
            concat_times = np.concat((prov_data.times, realtime_data.times), axis=0)
            concat_data = np.concat((prov_data.y, realtime_data.y), axis=0)
            store_data(return_name, data={'x': concat_times, 'y': concat_data}, attr_dict=prov_md)
            return_list.append(return_name)
        # if data type is not in either list, just ignore it
    del_data('kyoto_ae_tmp_*')
    return return_list



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
    realtime = False,
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
    realtime: bool
        If true, return data from the WDC realtime data directories, otherwise return provisional data.

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

        if realtime:
            ff = "%Y/%m/%d/" + datatype + "%y%m%d"
        else:
            ff = "%Y%m/" + datatype + "%y%m%d.for.request"

        try:
            file_names = dailynames(file_format=ff, trange=trange)
        except Exception as e:
            logging.error("Error occurred while getting file names: " + str(e))
            continue  # skip to the next datatype

        # Keep unique files names only
        file_names = list(set(file_names))
        # The above operation does not necessarily preserve order!  We need to sort the filenames.
        file_names = sorted(file_names)

        times = []
        data = []

        # Download the html page for each url and extract times and data
        for filename in file_names:
            if realtime:
                yyyy = filename[:4]
                mm = filename[5:7]
                dd = filename[8:10]
                url = remote_data_dir + "ae_realtime/data_dir/" + filename
                # Use a local path similar to IDL SPEDAS
                local_path = local_data_dir + "ae_realtime/data_dir/" + datatype + "/" + yyyy + "/" + mm + "/" + dd + "/"

            else:
                yyyymm = ""
                if len(filename) > 6:
                    yyyymm = filename[:6]
                url = remote_data_dir + "ae_provisional/" + filename
                # Use a local path similar to IDL SPEDAS
                local_path = local_data_dir + "ae_provisional/" + datatype + "/" + yyyymm + "/"
            fname = download(url, local_path=local_path, no_download=no_download, force_download=force_download)

            if download_only:
                continue  # skip to the next file

            if fname is None or len(fname) < 1:
                logging.error("Error occurred while downloading: " + url)
                continue  # skip to the next file
            try:
                with open(fname[0], "r") as file:
                    html_text = file.read()
                file_times, file_data = parse_ae_html(html_text)
                times.extend(file_times)
                data.extend(file_data)
            except Exception as e:
                logging.error(
                    "Error occurred while parsing " + filename + ": " + str(e)
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
    prov_cutoff_date = "2021-01-01/00:00:00"
    if time_double(trange[0]) >= time_double(prov_cutoff_date):
        retvalue = load_ae_worker(trange=trange,
                          datatypes=datatypes,
                          time_clip=time_clip,
                          remote_data_dir=remote_data_dir,
                          prefix=prefix,
                          suffix=suffix,
                          no_download=no_download,
                          local_data_dir=local_data_dir,
                          force_download=force_download,
                          realtime=True)
    elif time_double(trange[1]) < time_double(prov_cutoff_date):
        retvalue = load_ae_worker(trange=trange,
                          datatypes=datatypes,
                          time_clip=time_clip,
                          remote_data_dir=remote_data_dir,
                          prefix=prefix,
                          suffix=suffix,
                          no_download=no_download,
                          local_data_dir=local_data_dir,
                          force_download=force_download,
                          realtime=False)
    else:
        # Time range spans provisional/realtime cutoff
        del_data('kyoto_ae_tmp*')
        prov_trange = [trange[0],"2020-12-31:23:59:59"]
        realtime_trange = ["2021-01-01/00:00:00", trange[1]]
        prov_vars = load_ae_worker(trange=prov_trange,
                              datatypes=datatypes,
                              time_clip=time_clip,
                              remote_data_dir=remote_data_dir,
                              prefix='kyoto_ae_tmp_prov_',
                              suffix=suffix,
                              no_download=no_download,
                              local_data_dir=local_data_dir,
                              force_download=force_download,
                              realtime=False)
        realtime_vars = load_ae_worker(trange=realtime_trange,
                              datatypes=datatypes,
                              time_clip=time_clip,
                              remote_data_dir=remote_data_dir,
                              prefix='kyoto_ae_tmp_realtime_',
                              suffix=suffix,
                              no_download=no_download,
                              local_data_dir=local_data_dir,
                              force_download=force_download,
                              realtime=True)
        retvalue = merge_provisional_realtime(prov_vars,realtime_vars)

    # Print the acknowledgments
    logging.info(ack)
    return retvalue
