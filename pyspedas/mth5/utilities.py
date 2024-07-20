import urllib.request
import csv
import pyspedas
from io import StringIO
from collections import defaultdict
from pytplot import time_datetime


def _list_of_fdsn_channels():
    """
        Generates a list of channel names based on predefined bands, orientations, and a single instrument type.

        Returns
        -------
        str
            A string containing channel names, each separated by a comma. T

        Examples
        --------
        >>> _list_of_fdsn_channels()
        'MFZ,MFN,MFE,LFZ,LFN,LFE,VFZ,VFN,VFE,UFZ,UFN,UFE'
     """

    channel_band = ['M', 'L', 'V', 'U']
    channel_orientation = ['Z', 'N', 'E']
    # channel_orientation = ['Z', 'N', 'E', '1', '2'] # Some of the data can be stored as '1', '2', which is not supported byt this tool.
    channel_instrument = 'F'
    # Create list of all combinations of channel_band, channel_instrument and channel_orientation
    channel_list = ",".join(
        [f"{band}{channel_instrument}{orient}" for band in channel_band for orient in channel_orientation])
    return channel_list


def mth5_time_str(time):
    """
        Return pyspedas time format as  YYYY-MM-DDThh:mm:ss

        Parameters:
            time :  str
                Time in pytplot format

        Returns:
            Time in MTH5 format

    """
    return time_datetime(time).strftime("%Y-%m-%dT%H:%M:%S")


def datasets(trange=None, network=None, station=None, USAarea=False):
    """
    Fetches datasets availablity based on time range, network, and station.

    The function queries an FDSN (Federation of Digital Seismograph Networks) web service for station
    data within a specified time range and geographical bounds limited to the USA. It filters the resulting channels
    based on selection of 3 chanles of the same band and diffrent orienation, e.g., 'LFE', 'LFN', 'LFZ'. If the dataset has
    less than 3 channels with the same band, it is excluded. The resulting dataset is organized by network, station, and time
    range, including only the channels that meet the specified criteria.

    Parameters
    ----------
    trange : list of str
         Time range of interest [starttime, endtime] with the format ['YYYY-MM-DD','YYYY-MM-DD']
    network : str, optional
        The network code to filter the datasets. If None (default), no network filter is applied.
    station : str, optional
        The station code to filter the datasets. If None (default), no station filter is applied.
    USAarea : bool, optional
        If True, restricts the search to the geographical boundaries (box) of the USA:

        - Latitude: 24 to 49 degrees
        - Longitude: -127 to -59 degrees

    Returns
    -------
    dict
        A dictionary organized by network and station, each containing a dictionary of time ranges
        (start_date, end_date) mapping to a list of channels that meet the filter criteria. The
        dictionary is empty if no channels meet the criteria or if the inputs do not match any
        available data.

    Examples
    --------
    >>> datasets(["2015-06-22", "2015-06-23"], network="4P", station="ALW48")
    {'4P': {'ALW48': {('2015-06-18T15:00:36.0000', '2015-07-09T13:45:10.0000'): ['LFE', 'LFN', 'LFZ']}}}

    Note
    ----
    The function requires internet access to query the FDSN web service and parse the returned data.
    It uses the `urllib` library for the web request and the `csv` module to parse the response.
    """

    if not trange:
        return None

    # Function to filter channels based on the starting letter criteria
    def filter_channels_by_letter(channels):
        # Count channels starting with each letter
        channel_start_count = defaultdict(int)
        for channel in channels:
            if channel:  # Ensure the channel is not empty
                channel_start_count[channel[0]] += 1

        # Filter channels where the starting letter count is 3 or more
        return any(count >= 3 for count in channel_start_count.values())

    # Get data and handle empty response
    def fetch_data(url):
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return response.read().decode('utf-8')  # Or any other processing
                else:
                    pyspedas.logger.error("Server returned status code: %d", response.status)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            if hasattr(e, 'code') and e.code == 404:
                # No data
                return None
            else:
                pyspedas.logger.error("HTTP or URL Error encountered: %s", e)
        return None  # or an appropriate fallback value/error indicator

    t1 = mth5_time_str(trange[0])  # ["2019-11-14T00:00:00"],
    t2 = mth5_time_str(trange[1])  # ["2019-11-15T00:00:00"]

    # FDSN F Channels
    cha = _list_of_fdsn_channels()

    net_str = ''
    sta_str = ''
    if network:
        net_str = f'net={network}'

    if station:
        sta_str = f'sta={station}'

    if USAarea:
        # URL of the data limited to USA coordinate box
        # lat 24 49
        # lon -127 -59
        url = f'https://service.iris.edu/fdsnws/station/1/query?{net_str}&{sta_str}&loc=*&cha={cha}&starttime={t1}&endtime={t2}&level=channel&format=text&maxlat=49&minlon=-127&maxlon=-59&minlat=24&includecomments=false&nodata=404'
    else:
        # URL of the data unlimited in location
        url = f'https://service.iris.edu/fdsnws/station/1/query?{net_str}&{sta_str}&loc=*&cha={cha}&starttime={t1}&endtime={t2}&level=channel&format=text&includecomments=false&nodata=404'

    # Initialize the result dictionary
    res = {}

    # Fetching the data
    response_text = fetch_data(url)
    if response_text is not None:
        response_io = StringIO(response_text)

        reader = csv.reader(response_io, delimiter='|', skipinitialspace=True)
        reader.__next__()  # Skip the header row

        # Iterate over the rows in the reader object
        for row in reader:
            network, station, _, channel, *_, start_date, end_date = row

            # Initialize the network dictionary if not present
            if network not in res:
                res[network] = {}

            # Initialize the station dictionary within the network if not present
            if station not in res[network]:
                res[network][station] = {}

            # Use (start_date, end_date) tuple as a key, mapping to a list of channels
            date_tuple = (start_date, end_date)
            if date_tuple not in res[network][station]:
                res[network][station][date_tuple] = []

            # Append the current channel to the list for this date_tuple
            res[network][station][date_tuple].append(channel)
    else:
        return res

    # Filter the constructed dictionary, using copies of the iterators
    for network in list(res.keys()):
        for station in list(res[network].keys()):
            for date_tuple in list(res[network][station].keys()):
                channels = res[network][station][date_tuple]
                if not filter_channels_by_letter(channels):
                    del res[network][station][date_tuple]

            # Remove the station if it becomes empty after the filtering
            if not res[network][station]:
                del res[network][station]

        # Remove the network if it becomes empty after the filtering
        if not res[network]:
            del res[network]

    return res
