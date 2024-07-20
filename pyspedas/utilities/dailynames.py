import logging
import numpy as np
from pytplot import time_string, time_double
from datetime import datetime, timezone


def dailynames(directory='',
               trange=None,
               res=24*3600.,
               hour_res=False,
               file_format='%Y%m%d',
               prefix='',
               suffix='',
               return_times=False):
    """
    Creates a list of file names using a time range, resoution and file format
    Based on Davin Larson's file_dailynames in IDL SPEDAS

    Parameters:
        directory: str
            String containing the directory for the generated file names
            Default: ''. If directory is not specified the names will be written
            to the current working directory

        trange: list of str, list of datetime or list of floats
            Two-element list containing the start and end times for the file names
            Default: Current date. If the date range is not specified the routine will
            use the current date.

        res: float
            File name resolution in seconds
            Default: 24*3600., i.e., daily)

        file_format: str
            Format of the file names using strftime directives; for reference: https://strftime.org
            Default: %Y%m%d, i.e., daily

        prefix: str
            file name prefix
            Default: ''

        suffix: str
            file name suffix
            Default: ''

    Returns:
        List containing filenames

    Example:
        >>> from pyspedsas import time_float
        >>> time_range = time_float(['2021-01-01','2021-01-03'])
        >>> pyspedas.dailynames(trange=time_range)
    """
    if trange is None:
        logging.error('No trange specified')
        return

    if hour_res:
        res = 3600.
        file_format = '%Y%m%d%H'

    # allows the user to pass in trange as list of datetime objects
    if type(trange[0]) == datetime and type(trange[1]) == datetime:
        trange = [time_string(trange[0].replace(tzinfo=timezone.utc).timestamp()),
                  time_string(trange[1].replace(tzinfo=timezone.utc).timestamp())]

    tr = [trange[0], trange[1]]
    
    if isinstance(trange[0], str):
        tr[0] = time_double(trange[0])
    if isinstance(trange[1], str):
        tr[1] = time_double(trange[1])

    # Davin's magic heisted from file_dailynames in IDL
    mmtr = [np.floor(tr[0]/res), np.ceil(tr[1]/res)]

    if mmtr[1]-mmtr[0] < 1:
        n = 1
    else:
        n = int(mmtr[1]-mmtr[0])

    times = [(float(num)+mmtr[0])*res for num in range(n)]

    if return_times:
        return times

    dates = []
    files = []
        
    for time in times:
        if time_string(time, fmt=file_format) not in dates:
            dates.append(time_string(time, fmt=file_format))
            
    for date in dates:
        files.append(directory + prefix + date + suffix)

    return files

def yearlynames(
    trange,
    file_format="%Y%m%d",
    resolution="year",
    directory="",
    prefix="",
    suffix="",
):
    """
    Creates a list of file names using a time range, resolution, and file format.

    Parameters:
        trange: list of str or list of datetime
            Two-element list containing the start and end times for the file names.

        resolution: str
            Either 'year' or 'half-year' to determine the resolution.

        file_format: str
            Format of the file names using strftime directives.

        directory: str
            String containing the directory for the generated file names.

        prefix: str
            file name prefix.

        suffix: str
            file name suffix.

    Returns:
        List containing filenames.
    """

    if trange is None:
        raise ValueError("No trange specified")

    start_date = (
        trange[0]
        if isinstance(trange[0], datetime)
        else datetime.strptime(trange[0], "%Y-%m-%d")
    )
    end_date = (
        trange[1]
        if isinstance(trange[1], datetime)
        else datetime.strptime(trange[1], "%Y-%m-%d")
    )

    dates = []

    if resolution == "half-year":
        # Adjust the start date to be 6 months prior to the specified start date
        if start_date.month <= 6:
            adjusted_start_date = datetime(start_date.year - 1, start_date.month + 6, 1)
        else:
            adjusted_start_date = datetime(start_date.year, start_date.month - 6, 1)

        # Generate all the January 1st and July 1st dates within the range
        potential_dates = [datetime(year, month, 1) for year in range(start_date.year, end_date.year + 1) for month in [1, 7]]
        
        # Filter out dates outside the range
        dates = [date for date in potential_dates if adjusted_start_date < date <= end_date]
    elif resolution == "year":
        dates = [datetime(year, 1, 1) for year in range(start_date.year, end_date.year + 1)]
    else:
        raise ValueError("Invalid resolution specified. Choose 'year' or 'half-year'.")

    files = [directory + prefix + date.strftime(file_format) + suffix for date in dates]
    return files
