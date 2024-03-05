import urllib.request
import csv
from io import StringIO
from collections import defaultdict
from pyspedas.utilities.time_string import time_datetime

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


    pass