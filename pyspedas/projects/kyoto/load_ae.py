import logging
import re
from datetime import datetime, timedelta
from pytplot import time_clip as tclip
from pytplot import store_data, options
from pyspedas import dailynames, download
from .kyoto_config import CONFIG


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
            r"A\w{7}\s+(\d{6})\w(\d{2})(AE|AL|AO|AU|AX) \w{5}/\w\d{2}\s+(.*)", line
        )
        if match:
            date_str = match.group(1)
            hour_str = match.group(2)
            date = datetime.strptime(date_str + hour_str, "%y%m%d%H")
            minute_values = match.group(4).split()
            for i, value in enumerate(minute_values):
                if i >= 60:
                    break  # the last values is the daily mean
                date_times.append(date + timedelta(minutes=i))
                values.append(int(value))
    return date_times, values


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
    force_download=False
):
    """
    Downloads and loads provisional index data from the Kyoto World Data Center for Geomagnetism.

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
        logging.error("Keyword trange with two datetimes is required to download data.")
        return vars
    if trange[0] >= trange[1]:
        logging.error("Invalid time range. End time must be greater than start time.")
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

    all_datatypes = ["ae", "al", "ao", "au", "ax"]
    for i in range(len(datatypes)):
        datatype = datatypes[i].lower()
        if datatype not in all_datatypes:
            logging.error("Invalid datatype: " + datatype)
            continue  # skip to the next datatype

        ff = "%Y%m/" + datatype + "%y%m%d.for.request"
        try:
            file_names = dailynames(file_format=ff, trange=trange)
        except Exception as e:
            logging.error("Error occurred while getting file names: " + str(e))
            continue  # skip to the next datatype

        # Keep unique files names only
        file_names = list(set(file_names))

        times = []
        data = []

        # Download the html page for each url and extract times and data
        for filename in file_names:
            yyyymm = ""
            if len(filename) > 6:
                yyyymm = filename[:6]
            url = remote_data_dir + filename
            # Use a local path similar to IDL SPEDAS
            local_path = local_data_dir + datatype + "/" + yyyymm + "/"
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

    # Print the acknowledgments
    logging.info(ack)

    return vars
