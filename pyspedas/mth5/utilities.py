from pyspedas.utilities.time_string import time_datetime

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