from pyspedas.projects.mms.mms_load_data import mms_load_data
from pyspedas.projects.mms.edp_tools.mms_edp_set_metadata import mms_edp_set_metadata
from pyspedas.projects.mms.mms_config import CONFIG



def mms_load_edp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype='dce',
        varformat=None, varnames=[], get_support_data=False, suffix='', time_clip=True, no_update=False,
        available=False, notplot=False, latest_version=False, major_version=False, min_version=None, cdf_version=None, 
        spdf=False, always_prompt=False):
    """
    Load data from the MMS Electric field Double Probes (EDP) instrument
    
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

        data_rate : str or list of str
            instrument data rates for EDP include ['brst', 'fast', 'slow', 'srvy'].
            Default: 'fast'

        level : str
            indicates level of data processing.
            Default: 'l2'

        datatype : str or list of str
            Valid datatypes for EDP are: ['dce', 'dcv', 'ace', 'hmfe']
            Default: 'dce'

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".
            Default: False

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            Default: False
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables are loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded)
            Default: []

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.
            Default: None

        notplot: bool
            If True, then data are returned in a hash table instead of 
            being stored in tplot variables (useful for debugging, and
            access to multidimensional data products)
            Default: False

        available: bool
            If True, simply return the available data files (without downloading)
            for the requested parameters
            Default: False

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten
            Default: False

        cdf_version: str
            Specify a specific CDF version # to load (e.g., cdf_version='4.3.0')
            Default: None

        min_version: str
            Specify a minimum CDF version # to load
            Default: None

        latest_version: bool
            Only grab the latest CDF version in the requested time interval
            Default: False

        major_version: bool
            Only open the latest major CDF version (e.g., X in vX.Y.Z) in the requested time interval
            Default: False

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidentally save an incorrect password, or if your SDC password has changed
            Default: False

        spdf: bool
            If True, download the data from the SPDF instead of the SDC
            Default: False

    Returns
    --------
        list of str
            List of tplot variables created.

    Example
    -------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> edp_vars = pyspedas.projects.mms.mms_load_edp(trange=['2015-10-16', '2015-10-17'], probe='1')
    >>> tplot('mms1_edp_dce_gse_fast_l2')


    """

    # as of 20 June 2023, there's a mixture of v2.x.x and v3.x.x files at the SDC
    # these files aren't compatible, so we need to only load the latest major version
    # to avoid crashes (unless otherwise specified)
    if not latest_version and not major_version and min_version is None and cdf_version is None:
        major_version = True

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='edp',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, 
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, 
            always_prompt=always_prompt)
    
    if tvars is None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_edp_set_metadata(probe, data_rate, level, suffix=suffix)

    return tvars
