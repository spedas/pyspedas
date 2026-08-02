from .spd_mms_load_bss import spd_mms_load_bss

def make_data_rate_bars(trange=['2015-10-16', '2015-10-17'],
                     datatype=['fast', 'burst'],
                     probe='1',
                     suffix='',
                     no_download=False):
    """
    Creates tplot variables which allow you to display horizontal color bars 
    indicating fast or burst data availability.

    This is a convenience wrapper around spd_mms_load_bss.

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

    Examples
    --------
    
    >>> from pyspedas.projects.mms import make_data_rate_bars
    >>> from pyspedas import tplot
    >>> trange = ['2016-01-01', '2016-01-04']
    >>> vars = make_data_rate_bars(trange=trange)
    >>> tplot(vars)
    
    """
    return spd_mms_load_bss(trange=trange, probe=probe, datatype=datatype, suffix=suffix, no_download=no_download)
