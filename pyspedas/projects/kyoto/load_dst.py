import logging
import re
from pytplot import time_double, store_data, options, time_clip as tclip
from pyspedas import download, dailynames
from .kyoto_config import CONFIG


def parse_dst_html(html_text, year=None, month=None):
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
        hourly_data = re.findall(r'[-+]?\d+', day_str)
        ## if the data is not complete for a whole day (which is typically the case for real time data):
        if len(hourly_data[1:]) != 24:
            ## if the data is not completely missing for a whole day:
            if len(hourly_data[1:]) != 3:
                for idx, dst_value in enumerate(hourly_data[1:]):
                    ## The kyoto website uses a 4 digit format.
                    remainder = len(dst_value) % 4
                    ## if the remainder is not zero, it can be either the regular case '-23' or
                    ## the ill case '-159999'. index by 0:remainder gives the correct -23 or -15
                    if remainder > 0:
                        times.append(
                            time_double(
                                year + "-" + month + "-" + hourly_data[0] + "/" + str(idx) + ":30"
                            )
                        )
                        data.append(float(dst_value[0:remainder]))
                    ## if the remainder is zero, it can be either the regular case '-1599999' or
                    ## the ill case '9999...9999' with the number of nine being the multiple of 4.
                    ## we further test if the first four digits are 9999. If not, we simply index by
                    ## [0:4], which gives -159 in the regular case. Else, we ignore missing data.
                    elif dst_value[0:4] != '9999':
                        times.append(
                            time_double(
                                year + "-" + month + "-" + hourly_data[0] + "/" + str(idx) + ":30"
                            )
                        )
                        data.append(float(dst_value[0:4]))
        ## if the data is complete for a whole day.
        else:
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
    datatypes=["final", "provisional", "realtime"],
    time_clip=True,
    remote_data_dir="http://wdc.kugi.kyoto-u.ac.jp/",
    prefix="",
    suffix="",
    no_download=False,
    local_data_dir="",
    download_only=False,
    force_download=False,
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
    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------
    list of str
        List of tplot variables created.

    Notes
    -----
    There are three types of Dst data available: final, provisional, and realtime.
    Usually, only one type is available for a particular month.
    is function tries to download final data, if this is not available then
    it downloads provisional data, and if this is not available then it downloads
    realtime data.

    Examples
    --------
    >>> from pyspedas.projects.kyoto import dst
    >>> dst_data = dst(trange=['2015-01-01', '2015-01-02'])
    >>> print(dst_data)
    kyoto_dst
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
        remote_data_dir = CONFIG["remote_data_dir_dst"]

    try:
        file_names = dailynames(file_format="%Y%m/index.html", trange=trange)
    except Exception as e:
        logging.error("Error occurred while getting file names: " + str(e))
        return vars

    # Keep unique files names only
    file_names = list(set(file_names))

    ack = """
            ******************************
            The DST data are provided by the World Data Center for Geomagnetism, Kyoto, and
            are not for redistribution (http://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank
            the geomagnetic observatories (Kakioka [JMA], Honolulu and San Juan [USGS], Hermanus
            [RSA], Alibag [IIG]), NiCT, INTERMAGNET, and many others for their cooperation to
            make the Dst index available.
            ******************************
        """

    times = []
    data = []
    datatypes = ["final", "provisional", "realtime"]

    # Final files
    for datatype in datatypes:

        for filename in file_names:
            yyyymm = ""
            if len(filename) > 6:
                yyyymm = filename[:6]
            url = remote_data_dir + "dst_" + datatype + "/" + filename
            local_path = local_data_dir + "dst_" + datatype + "/" + yyyymm + "/"
            fname = download(
                url, local_path=local_path, no_download=no_download, text_only=True, force_download=force_download,
            )

            if download_only:
                continue  # skip to the next file

            if fname is None or len(fname) < 1:
                logging.error("Error occurred while downloading: " + url)
                continue  # skip to the next file
            try:
                with open(fname[0], "r") as file:
                    html_text = file.read()
                file_times, file_data = parse_dst_html(
                    html_text, year=filename[:4], month=filename[4:6]
                )
                times.extend(file_times)
                data.extend(file_data)
            except Exception as e:
                logging.error(
                    "Error occurred while parsing " + filename + ": " + str(e)
                )
                continue  # skip to the next file

        # At this point, we have all data for one datatype
        # If we have data, we can break the loop, otherwise we try other datatypes
        if len(times) != 0:
            break

    if len(times) == 0:
        logging.error("No data found.")
        return vars

    varname = prefix + "kyoto_dst" + suffix
    store_data(varname, data={"x": times, "y": data})
    options(varname, "ytitle", "Dst (" + datatype + ")")
    vars.append(varname)

    if time_clip:
        tclip(varname, trange[0], trange[1], overwrite=True)

    logging.info(ack)

    return vars
