import logging
from pyspedas.projects.mms.mms_load_fast_intervals import mms_load_fast_intervals
from pyspedas.projects.mms.mms_load_burst_intervals import mms_load_burst_intervals
from .make_databar_tvar import make_databar_tvar


def spd_mms_load_bss(trange=['2015-10-16', '2015-10-17'],
                     datatype=['fast', 'burst'],
                     probe='1',
                     suffix='',
                     no_download=False):
    """
    Creates tplot variables which allow you to display horizontal color bars 
    indicating fast or burst data availability.

    Parameters
    -----------
        trange: list of str
            Time frame for the bars

        datatype: str or list of str
            Type of BSS data (current valid options: 'fast', 'burst')

        probe: str or int
            S/C probe # for SRoI bars (used as fast survey segments after 6Nov15; default: 1)

        suffix: str
            Suffix to add to tplot variable names. Default: ''

        no_download: bool
            If True, use cached files rather than downloading from the MMS SDC
            Default: False

    Returns
    -------
    list[str]
        List of tplot variables created

    """

    if not isinstance(datatype, list):
        datatype = [datatype]

    tvars_created = []
    
    for dtype in datatype:
        if dtype == 'fast':
            out = mms_load_fast_intervals(trange=trange, probe=probe, no_download=no_download)
            if (out is None) or (len(out[0]) == 0):
                logging.error("Problem loading fast survey intervals")
            else:
                tvar = make_databar_tvar(basename='mms_bss_fast',label='Fast',suffix=suffix,unix_starts=out[0],unix_ends=out[1])
                tvars_created.append(tvar)
        elif dtype == 'burst':
            out = mms_load_burst_intervals(trange=trange, no_download=no_download)
            if (out is None) or (len(out[0]) == 0):
                logging.error("Problem loading burst intervals")
            else:
                tvar = make_databar_tvar(basename="mms_bss_burst", suffix=suffix, label='Burst',unix_starts=out[0], unix_ends=out[1])
                tvars_created.append(tvar)
        else:
            logging.error('Unsupported datatype: ' + dtype + '; valid options: "fast" and "burst"')
            continue

    return tvars_created