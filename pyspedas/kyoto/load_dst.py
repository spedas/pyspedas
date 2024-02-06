import logging
import requests
from pytplot import time_double
from pytplot import time_clip as tclip
from pytplot import store_data, options
from pyspedas.utilities.dailynames import dailynames
import re


def parse_html(html_text, year=None, month=None):
    """
    Parses the HTML content to extract relevant information.

    Parameters
    ----------
    html_text : str
        The HTML content to parse.
    year : int, optional
        The year to consider while parsing the HTML content. If not provided, all years are considered.
    month : int, optional
        The month to consider while parsing the HTML content. If not provided, all months are considered.

    Returns
    -------
    dict
        A dictionary containing the parsed information.
    """
    times = []
    data = []
    # remove all of the HTML before the table
    html_data = html_text[html_text.find("Hourly Equatorial Dst Values") :]
    # remove all of the HTML after the table
    html_data = html_data[: html_data.find("<!-- vvvvv S yyyymm_part3.html vvvvv -->")]
    html_lines = html_data.split("\n")
    data_strs = html_lines[5:]
    # loop over days
    for day_str in data_strs:
        # the first element of hourly_data is the day, the rest are the hourly Dst values
        #         hourly_data = day_str.split()
        hourly_data = re.findall(r"[-+]?\d+", day_str)
        if len(hourly_data[1:]) != 24:
            continue
        for idx, dst_value in enumerate(hourly_data[1:]):
            times.append(
                time_double(
                    year + "-" + month + "-" + hourly_data[0] + "/" + str(idx) + ":30"
                )
            )
            data.append(float(dst_value))

    return (times, data)


def dst(
    trange=None,
    time_clip=True,
    remote_data_dir="http://wdc.kugi.kyoto-u.ac.jp/",
    suffix="",
):
    """
    Loads Dst index data from the Kyoto servers.

    Parameters
    ----------
    trange : list of str, required
        Time range of interest with the format ['YYYY-MM-DD','YYYY-MM-DD'] or
        to specify more or less than a day ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
        Defaults to True.
    remote_data_dir : str, optional
        The remote directory from where to load the Dst index data.
        Defaults to "http://wdc.kugi.kyoto-u.ac.jp/".
    suffix : str, optional
        The tplot variable names will be given this suffix.
        By default, no suffix is added.

    Returns
    -------
    list
        List of tplot variables created.

    Examples
    --------
    >>> from pyspedas.kyoto import dst
    >>> dst_data = dst(trange=['2015-01-01', '2015-01-02'])
    >>> print(dst_data)
    kyoto_dst

    Acknowledgment
    --------------
        The DST data are provided by the World Data Center for Geomagnetism, Kyoto, and
        are not for redistribution (http://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank
        the geomagnetic observatories (Kakioka [JMA], Honolulu and San Juan [USGS], Hermanus
        [RSA], Alibag [IIG]), NiCT, INTERMAGNET, and many others for their cooperation to
        make the Dst index available.
    """

    if trange is None:
        logging.error("trange keyword required to download data.")
        return

    try:
        file_names = dailynames(file_format="%Y%m/index.html", trange=trange)
    except Exception as e:
        logging.error("Error occurred while getting file names: " + str(e))
        return

    times = []
    data = []
    datatype = ""

    # Final files
    for filename in file_names:
        html_text = requests.get(remote_data_dir + "dst_final/" + filename).text
        file_times, file_data = parse_html(
            html_text, year=filename[:4], month=filename[4:6]
        )
        times.extend(file_times)
        data.extend(file_data)
        if len(file_times) != 0:
            datatype = "Final"

    # Provisional files
    for filename in file_names:
        html_text = requests.get(remote_data_dir + "dst_provisional/" + filename).text
        file_times, file_data = parse_html(
            html_text, year=filename[:4], month=filename[4:6]
        )
        times.extend(file_times)
        data.extend(file_data)
        if len(file_times) != 0:
            datatype = "Provisional"

    # Real Time files
    for filename in file_names:
        html_text = requests.get(remote_data_dir + "dst_realtime/" + filename).text
        file_times, file_data = parse_html(
            html_text, year=filename[:4], month=filename[4:6]
        )
        times.extend(file_times)
        data.extend(file_data)
        if len(file_times) != 0:
            datatype = "Real Time"

    if len(times) == 0:
        logging.error("No data found.")
        return

    store_data("kyoto_dst" + suffix, data={"x": times, "y": data})

    if time_clip:
        tclip("kyoto_dst" + suffix, trange[0], trange[1], suffix="")

    options("kyoto_dst" + suffix, "ytitle", "Dst (" + datatype + ")")

    logging.info(
        "**************************************************************************************"
    )
    logging.info(
        "The DST data are provided by the World Data Center for Geomagnetism, Kyoto, and"
    )
    logging.info(
        " are not for redistribution (http://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank"
    )
    logging.info(
        " the geomagnetic observatories (Kakioka [JMA], Honolulu and San Juan [USGS], Hermanus"
    )
    logging.info(
        " [RSA], Alibag [IIG]), NiCT, INTERMAGNET, and many others for their cooperation to"
    )
    logging.info(" make the Dst index available.")
    logging.info(
        "**************************************************************************************"
    )

    return "kyoto_dst" + suffix
