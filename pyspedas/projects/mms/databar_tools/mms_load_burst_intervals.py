from pyspedas.projects.mms.databar_tools.mms_load_brst_segments import mms_load_brst_segments

def mms_load_burst_intervals(trange=['2015-10-16', '2015-10-17'],
                     probe='1',
                     no_download=False):
    """
    Load time intervals of burst data availability

    Parameters
    -----------
        trange: list of str
            Time frame for the bars

        probe: str or int
            S/C probe # for SRoI bars (used as fast survey segments after 6Nov15; default: 1)

        no_download: bool
            If True, use cached files rather than downloading from the MMS SDC

    Returns
    -------
    tuple
        Tuple of start times, end times of burst segments.

    Examples
    --------

    >>> from pyspedas.projects.mms import mms_load_burst_intervals
    >>> from pyspedas import time_string
    >>> trange = ['2016-01-01/00:00:00', '2016-01-01/01:00:00']
    >>> starts, ends = mms_load_burst_intervals(trange=trange)
    >>> n = len(starts)
    >>> for idx in range(n):
    >>>     print(f"Burst interval {idx+1} of {n}, start: {time_string(starts[idx])} end: {time_string(ends[idx])}")
    Burst interval 1 of 4, start: 2016-01-01 00:56:44.000000 end: 2016-01-01 00:57:34.000000
    Burst interval 2 of 4, start: 2016-01-01 00:57:34.000000 end: 2016-01-01 00:58:24.000000
    Burst interval 3 of 4, start: 2016-01-01 00:58:24.000000 end: 2016-01-01 00:59:14.000000
    Burst interval 4 of 4, start: 2016-01-01 00:59:14.000000 end: 2016-01-01 01:00:04.000000

    """

    return mms_load_brst_segments(trange=trange, no_download=no_download)
