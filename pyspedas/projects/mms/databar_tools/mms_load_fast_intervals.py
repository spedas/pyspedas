import logging
from pyspedas.tplot_tools import time_double
from pyspedas.projects.mms.databar_tools.mms_load_sroi_segments import mms_load_sroi_segments
from pyspedas.projects.mms.databar_tools.mms_update_fast_intervals import mms_update_fast_intervals


def mms_load_fast_intervals(trange=['2015-10-16', '2015-10-17'],
                     probe='1',
                     no_download=False):
    """
    Load MMS fast survey time intervals

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
        A tuple containing arrays of start times and end times for each fast survey interval in the included time range.

    Examples
    --------
    
    >>> from pyspedas.projects.mms import mms_load_fast_intervals
    >>> from pyspedas import time_string
    >>> trange = ['2016-01-01', '2016-01-04']
    >>> starts, ends = mms_load_fast_intervals(trange=trange)
    >>> n = len(starts)
    >>> for idx in range(n):
    >>>     print(f"Fast survey interval {idx+1} of {n}, start: {time_string(starts[idx])} end: {time_string(ends[idx])}")
    Fast survey interval 1 of 4, start: 2015-12-31 21:26:09.000000 end: 2016-01-01 10:34:59.000000
    Fast survey interval 2 of 4, start: 2016-01-01 21:19:11.000000 end: 2016-01-02 10:28:03.000000
    Fast survey interval 3 of 4, start: 2016-01-02 21:12:13.000000 end: 2016-01-03 10:21:11.000000
    Fast survey interval 4 of 4, start: 2016-01-03 21:05:16.000000 end: 2016-01-04 10:14:22.000000

    """


    abs_sroi_cutover = time_double('2015-11-06')
    if time_double(trange[0]) <= abs_sroi_cutover and time_double(trange[1]) <= abs_sroi_cutover:
        # use the old fast segments code for dates before 6Nov15
        logging.info("Loading early mission fast survey segments from abs_selections datasets")
        out = mms_update_fast_intervals(trange=trange,no_download=no_download)
    elif time_double(trange[0]) <= abs_sroi_cutover and time_double(trange[1]) > abs_sroi_cutover:
        # Requested range spans cutover date, get ABS before and SROI after, then combine
        out1 = mms_update_fast_intervals(trange=[trange[0],abs_sroi_cutover], no_download=no_download)
        out2 = mms_load_sroi_segments(trange=trange, probe=probe,no_download=no_download)
        comb_starts = []
        comb_ends = []
        if out1 is not None:
            comb_starts.extend(out1[0])
            comb_ends.extend(out1[1])
        if out2 is not None:
            comb_starts.extend(out2[0])
            comb_ends.extend(out2[1])
        # make the tplot variable
        out = comb_starts, comb_ends

    else:
        # use SRoI code for dates on and after 6Nov15
        out = mms_load_sroi_segments(trange=trange, probe=probe)

    if out is None:
        logging.error('Problem loading fast survey segment times')
        return None

    return out
