import urllib.request
import csv
import pyspedas
from io import StringIO
from collections import defaultdict
from pyspedas.tplot_tools import time_datetime


def _list_of_fdsn_channels(instruments='F'):
    """
        Generates a list of channel names based on predefined bands, orientations, and instrument types.

        Parameters
        ----------
        instruments : str, default='F'
            SEED instrument codes, one character each: 'F' (magnetic), 'Q' (electric), or 'FQ' (both).

        Returns
        -------
        str
            A string containing channel names, each separated by a comma.

        Examples
        --------
        >>> _list_of_fdsn_channels()
        'MFZ,MFN,MFE,MF1,MF2,MF3,LFZ,LFN,LFE,LF1,LF2,LF3,VFZ,VFN,VFE,VF1,VF2,VF3,UFZ,UFN,UFE,UF1,UF2,UF3'
     """

    # TODO: modify according to SEED manual appendix A: https://www.fdsn.org/pdf/SEEDManual_V2.4_Appendix-A.pdf
    channel_band = ['M', 'L', 'V', 'U']
    # 'Z', 'N', 'E' (vertical, north, east) and '1', '2', '3' (numeric
    # orientations some stations use instead) both map to MTH5's
    # hx/hy/hz components for instrument code F. See fdsn_data_model.md.
    channel_orientation = ['Z', 'N', 'E', '1', '2', '3']
    # Create list of all combinations of channel_instrument, channel_band and channel_orientation
    channel_list = ",".join(
        [f"{band}{channel_instrument}{orient}" for channel_instrument in instruments
         for band in channel_band for orient in channel_orientation])
    return channel_list


def mth5_time_str(time):
    """
        Return pyspedas time format as YYYY-MM-DDThh:mm:ss

        Parameters:
            time : str
                Time in pyspedas format

        Returns:
            Time in MTH5 format

    """
    return time_datetime(time).strftime("%Y-%m-%dT%H:%M:%S")


def _print_datasets(res):
    """
    Print the result of `datasets` as one row per time range, listing the channels that share it.

    Parameters
    ----------
    res : dict
        Output of `datasets`, e.g.
        {'8P': {'CAS04': {('2020-06-02T18:41:43.0000', '2020-07-13T21:46:12.0000'): ['LFE', 'LFN', 'LFZ']}}}

    Examples
    --------
    >>> _print_datasets(res)
    8P CAS04
      Channels      Start                      End
      LFE,LFN,LFZ   2020-06-02T18:41:43.0000   2020-07-13T21:46:12.0000
    """
    if not res:
        print("No datasets found")
        return

    for network, stations in res.items():
        for station, time_ranges in stations.items():
            print(f"{network} {station}")
            # One (channels, start, end) row per time range, e.g. ('LFE,LFN,LFZ', start, end),
            # sorted by channels and then start time
            rows = sorted(
                (','.join(channels), start, end)
                for (start, end), channels in time_ranges.items()
            )
            # Channels column fits the longest channel list, e.g. 'LFE,LFN,LFZ'
            width = max(len('Channels'), max(len(row[0]) for row in rows)) + 2
            print(f"  {'Channels':{width}} {'Start':26} End")
            for channels, start, end in rows:
                print(f"  {channels:{width}} {start:26} {end}")


def datasets(trange=None, network=None, station=None, USAarea=False, datatype='mag', keep_incomplete=False,
             quiet=True):
    """
    Fetches datasets availability based on time range, network, and station.

    The function queries an FDSN (Federation of Digital Seismograph Networks) web service for station
    data within a specified time range and geographical bounds limited to the USA. It filters the resulting channels
    based on selection of 3 magnetic channels of the same band and different orientation, e.g., 'LFE', 'LFN', 'LFZ',
    or 2 electric channels, e.g., 'LQE', 'LQN'. A time range without such a complete set is excluded. The resulting
    dataset is organized by network, station, and time range, including only the channels that meet the specified criteria.

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
    datatype : str or list of str, default='mag'
        Physical field(s) to search for: 'mag' (magnetic, SEED instrument code F), 'elec' (electric, Q),
        or ['mag', 'elec'].
    keep_incomplete : bool, default=False
        If True, don't remove time ranges without a complete set of channels. Every channel epoch
        is kept, e.g. electric channels whose epochs are split at different times.
    quiet : bool, default=True
        If False, print the result as one row per channel and time range.

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

    # SEED instrument code and the number of channels in a complete set, per datatype
    instrument_codes = {'mag': 'F', 'elec': 'Q'}
    complete_set = {'F': 3, 'Q': 2}  # e.g. LFE, LFN, LFZ or LQE, LQN

    # Normalize datatype to a list, e.g. 'mag' -> ['mag']
    datatypes = [datatype] if isinstance(datatype, str) else list(datatype)
    if not datatypes or any(d not in instrument_codes for d in datatypes):
        pyspedas.logger.error(f"Invalid datatype {datatype}. Use 'mag', 'elec' or ['mag', 'elec']")
        return None
    # e.g. ['mag', 'elec'] -> 'FQ'
    instruments = ''.join(sorted({instrument_codes[d] for d in datatypes}))

    # Function to filter channels based on the band and instrument criteria
    def filter_channels_by_letter(channels):
        # Count channels per band and instrument, e.g. 'LF' for LFE
        channel_start_count = defaultdict(int)
        for channel in channels:
            if channel:  # Ensure the channel is not empty
                channel_start_count[channel[:2]] += 1

        # Keep the time range if at least one band and instrument has a complete set,
        # e.g. {'LF': 3} -> True, {'LQ': 1} -> False
        return any(count >= complete_set.get(key[1:], 3) for key, count in channel_start_count.items())

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

    # FDSN channels of the requested instruments, e.g. F (magnetic) and Q (electric)
    cha = _list_of_fdsn_channels(instruments=instruments)

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
        url = f'https://service.earthscope.org/fdsnws/station/1/query?{net_str}&{sta_str}&loc=*&cha={cha}&starttime={t1}&endtime={t2}&level=channel&format=text&maxlat=49&minlon=-127&maxlon=-59&minlat=24&includecomments=false&nodata=404'
    else:
        # URL of the data unlimited in location
        url = f'https://service.earthscope.org/fdsnws/station/1/query?{net_str}&{sta_str}&loc=*&cha={cha}&starttime={t1}&endtime={t2}&level=channel&format=text&includecomments=false&nodata=404'

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
        if not quiet:
            _print_datasets(res)
        return res

    # Filter the constructed dictionary, using copies of the iterators
    for network in list(res.keys()):
        for station in list(res[network].keys()):
            for date_tuple in list(res[network][station].keys()):
                channels = res[network][station][date_tuple]
                if not keep_incomplete and not filter_channels_by_letter(channels):
                    del res[network][station][date_tuple]

            # Remove the station if it becomes empty after the filtering
            if not res[network][station]:
                del res[network][station]

        # Remove the network if it becomes empty after the filtering
        if not res[network]:
            del res[network]

    if not quiet:
        _print_datasets(res)

    return res
