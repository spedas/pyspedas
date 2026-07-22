import logging
from pyspedas.tplot_tools import time_double
from pyspedas.projects.mms.mms_load_sroi_segments import mms_load_sroi_segments
from pyspedas.projects.mms.mms_load_brst_segments import mms_load_brst_segments
from pyspedas.projects.mms.mms_update_fast_intervals import mms_update_fast_intervals
from .make_bss_tplot_var import make_bss_tplot_var


def spd_mms_load_bss(trange=['2015-10-16', '2015-10-17'], datatype=['fast', 'burst'], 
                     include_labels=False, probe='1',suffix='',
                     nodownload=False):
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
            abs_sroi_cutover = time_double('2015-11-06')
            if time_double(trange[0]) <= abs_sroi_cutover and time_double(trange[1]) <= abs_sroi_cutover:
                # use the old fast segments code for dates before 6Nov15
                logging.info("Loading early mission fast survey segments from abs_selections datasets")
                out = mms_update_fast_intervals(trange=trange,suffix=suffix,label=fast_label,nodownload=nodownload)

            elif time_double(trange[0]) <= abs_sroi_cutover and time_double(trange[1]) > abs_sroi_cutover:
                # Requested range spans cutover date, get ABS before and SROI after, then combine
                out1 = mms_update_fast_intervals(trange=[trange[0],abs_sroi_cutover], make_tplot_var=False, nodownload=nodownload)
                out2 = mms_load_sroi_segments(trange=trange, probe=probe, make_tplot_var=False,nodownload=nodownload)
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
                make_bss_tplot_var(out[0],out[1],suffix=suffix,label=fast_label)

            else:
                # use SRoI code for dates on and after 6Nov15
                out = mms_load_sroi_segments(trange=trange, probe=probe, suffix=suffix, label=fast_label)
        elif dtype == 'burst':
            out = mms_load_brst_segments(trange=trange)
        else:
            logging.error('Unsupported datatype: ' + dtype + '; valid options: "fast" and "burst"')
            continue

        if out is None:
            logging.error('Problem loading segments for ' + dtype)
