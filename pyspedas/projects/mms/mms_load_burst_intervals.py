from pyspedas.projects.mms.mms_load_brst_segments import mms_load_brst_segments

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

    """

    return mms_load_brst_segments(trange=trange, no_download=no_download)
