from pyspedas.projects.mms.mec_ascii.mms_get_tetrahedron_qf import mms_get_tetrahedron_qf



def mms_load_tetrahedron_qf(trange=['2015-10-16', '2015-10-17'], no_update=False, suffix=''):
    """
    Load the MMS tetrahedron quality factor data from the ASCII files
    into tplot variables
    
    Parameters
    ----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2015-10-16', '2015-10-17']

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.
            Default: None

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten
            Default: False

    Returns
    --------
        list of str
            List of tplot variables created.

    Example
    -------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> qf_vars = pyspedas.projects.mms.mms_load_tetrahedron_qf(trange=['2015-10-16', '2015-10-17'])
    >>> tplot('mms_tetrahedron_qf')

    """
    return mms_get_tetrahedron_qf(trange=trange, no_download=no_update, suffix=suffix)
