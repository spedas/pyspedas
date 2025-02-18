from pyspedas.projects.mms.mec_ascii.mms_get_state_data import mms_get_state_data



def mms_load_state(trange=['2015-10-16', '2015-10-17'], probe='1', level='def',
    datatypes=['pos', 'vel'], no_update=False, pred_or_def=True, suffix=''):
    """
    This function loads the state (ephemeris and attitude) data from the ASCII files 
    into tplot variables
    
    Parameters
    ----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2015-10-16', '2015-10-17']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4'].
            Default: '1'

        level : str
            indicates level of data (options: 'def' (definitive), 'pred' (predicted)
            Default: 'def'

        datatypes : str or list of str
            Datatypes for state data to be loaded (options: 'pos', 'vel', 'spinras', 'spindec')
            Default: ['pos', 'vel']

        suffix: str
            The tplot variable names will be given this suffix.
            Default: None

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten
            Default: False

        pred_or_def: bool
            Load definitive or predicted (if definitive isn't available); defaults to True
            Default: True

    Returns
    --------
        list of str
            List of tplot variables created.

    Example
    -------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> pos_data = pyspedas.projects.mms.mms_load_state(trange=['2015-10-16', '2015-10-17'], probe='1', datatypes='pos', level='def')
    >>> tplot('mms1_defeph_pos')


    """
    return mms_get_state_data(trange=trange, probe=probe, level=level, datatypes=datatypes,
        no_download=no_update, pred_or_def=pred_or_def, suffix=suffix)
