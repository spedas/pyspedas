import logging
from pyspedas.tplot_tools import time_double
from pyspedas.projects.mms.mms_load_sroi_segments import mms_load_sroi_segments
from pyspedas.projects.mms.mms_load_brst_segments import mms_load_brst_segments
from pyspedas.projects.mms.mms_update_fast_intervals import mms_update_fast_intervals
from .make_bss_tplot_var import make_bss_tplot_var


def spd_mms_load_bss(trange=['2015-10-16', '2015-10-17'],
                     datatype=['fast', 'burst'],
                     probe='1',suffix='',
                     no_download=False):
    """
    Creates tplot variables which allow you to display horizontal color bars 
    indicating burst data availability.

    Parameters
    -----------
        trange: list of str
            Time frame for the bars

        datatype: str or list of str
            Type of BSS data (current valid options: 'fast', 'burst')

        probe: str or int
            S/C probe # for SRoI bars (used as fast survey segments after 6Nov15; default: 1)

        no_download: bool
            If True, use cached files rather than downloading from the MMS SDC

    """

    if not isinstance(datatype, list):
        datatype = [datatype]

    for dtype in datatype:
        if dtype == 'fast':
            abs_sroi_cutover = time_double('2015-11-06')
            if time_double(trange[0]) <= abs_sroi_cutover and time_double(trange[1]) <= abs_sroi_cutover:
                # use the old fast segments code for dates before 6Nov15
                logging.info("Loading early mission fast survey segments from abs_selections datasets")
                out = mms_update_fast_intervals(trange=trange,suffix=suffix,no_download=no_download)

            elif time_double(trange[0]) <= abs_sroi_cutover and time_double(trange[1]) > abs_sroi_cutover:
                # Requested range spans cutover date, get ABS before and SROI after, then combine
                out1 = mms_update_fast_intervals(trange=[trange[0],abs_sroi_cutover], make_tplot_var=False, no_download=no_download)
                out2 = mms_load_sroi_segments(trange=trange, probe=probe, make_tplot_var=False,no_download=no_download)
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
                make_bss_tplot_var(out[0],out[1],suffix=suffix)

            else:
                # use SRoI code for dates on and after 6Nov15
                out = mms_load_sroi_segments(trange=trange, probe=probe, suffix=suffix)
        elif dtype == 'burst':
            out = mms_load_brst_segments(trange=trange, suffix=suffix, no_download=no_download)
        else:
            logging.error('Unsupported datatype: ' + dtype + '; valid options: "fast" and "burst"')
            continue

        if out is None:
            logging.error('Problem loading segments for ' + dtype)
