from pyspedas.mms.mec_ascii.mms_get_tetrahedron_qf import mms_get_tetrahedron_qf
from pyspedas.mms.print_vars import print_vars


@print_vars
def mms_load_tetrahedron_qf(trange=['2015-10-16', '2015-10-17'], no_update=False, suffix=''):
    """
    This function loads the MMS tetrahedron quality factor data from the ASCII files
    into tplot variables
    
    Parameters
    ----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten

    Returns
    --------
        List of tplot variables created.

    """
    return mms_get_tetrahedron_qf(trange=trange, no_download=no_update, suffix=suffix)
