import logging
from pyspedas import time_double
from pyspedas.mms.mms_load_fast_segments import mms_load_fast_segments
from pyspedas.mms.mms_load_sroi_segments import mms_load_sroi_segments
from pyspedas.mms.mms_load_brst_segments import mms_load_brst_segments


def spd_mms_load_bss(trange=['2015-10-16', '2015-10-17'], datatype=['fast', 'burst'], 
                     include_labels=False, probe='1', nodownload=False):
    """
    Creates tplot variables which allow you to display horizontal color bars 
    indicating burst data availability.

    Parameters
    -----------
        trange: list of str
            Time frame for the bars

        datatype: str or list of str
            Type of BSS data (current valid options: 'fast', 'burst')

        include_labels: bool
            Flag to have horizontal bars labeled

        probe: str or int
            S/C probe # for SRoI bars (used as fast survey segments after 6Nov15; default: 1)
    """

    if not isinstance(datatype, list):
        datatype = [datatype]

    if include_labels:
        burst_label = 'Burst'
        fast_label = 'Fast'
    else:
        burst_label = ''
        fast_label = ''

    for dtype in datatype:
        if dtype == 'fast':
            if time_double(trange[0]) <= time_double('2015-11-06'):
                # use the old fast segments code for dates before 6Nov15
                out = mms_load_fast_segments(trange=trange)
            else:
                # use SRoI code for dates on and after 6Nov15
                out = mms_load_sroi_segments(trange=trange, probe=probe)
        elif dtype == 'burst':
            out = mms_load_brst_segments(trange=trange)
        else:
            logging.error('Unsupported datatype: ' + dtype + '; valid options: "fast" and "burst"')
            continue

        if out is None:
            logging.error('Problem loading segments for ' + dtype)
