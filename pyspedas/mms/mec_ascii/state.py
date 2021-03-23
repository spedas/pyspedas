
from pyspedas.mms.mec_ascii.mms_get_state_data import mms_get_state_data
from pyspedas.mms.print_vars import print_vars

@print_vars
def mms_load_state(trange=['2015-10-16', '2015-10-17'], probe='1', level='def',
    datatypes=['pos', 'vel'], no_update=False, pred_or_def=True, suffix=''):
    """
    This function loads the state (ephemeris and attitude) data from the ASCII files 
    into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        level : str
            indicates level of data (options: 'def' (definitive), 'pred' (predicted); default: def)

        datatypes : str or list of str
            no datatype for state data (options: 'pos', 'vel', 'spinras', 'spindec')

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten

    Returns:
        List of tplot variables created.

    """
    return mms_get_state_data(trange=trange, probe=probe, level=level, datatypes=datatypes,
        no_download=no_update, pred_or_def=pred_or_def, suffix=suffix)
