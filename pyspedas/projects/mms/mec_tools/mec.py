from pyspedas.projects.mms.mms_load_data import mms_load_data
from pyspedas.projects.mms.mec_tools.mms_mec_set_metadata import mms_mec_set_metadata
from pyspedas.projects.mms.mms_config import CONFIG


def mms_load_mec(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='epht89q', varformat=None, varnames=[], suffix='', get_support_data=False,
    time_clip=False, no_update=False, available=False, notplot=False, latest_version=False, 
    major_version=False, min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    Load the attitude/ephemeris data from the MMS MEC (Mission Ephemeris and Coordinates) files
    
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
            instrument data rates for MEC include ['brst', 'srvy'].
            Default: 'srvy'

        level : str
            indicates level of data processing.
            Default: 'l2'

        datatype : str or list of str
            Valid datatypes for MEC are: ['ephts04d', 'epht89q', 'epht89d']
            Default: 'epht89q'

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            Default: False
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables are loaded)

        varnames: list of str
            List of variable names to load. If list is empyt or not specified,
            all data variables are loaded)
            Default: [] (all variables are loaded)

        suffix: str
            The tplot variable names will be given this suffix.
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
    
    Notes
    ---------
        The default datatype was changed to 'epht89q' on 15Nov2021. There are sometimes issues with 
        creating the Tsyganenko 04 data products, which leads to the 'epht04d' files not being available. 
        The 'epht89d' files contain the same ephemeris data - the only difference are the data products
        that rely on the field model. 
        
    Returns
    -------
        list of str
            List of tplot variables created.

    Example
    -------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> mec_data = pyspedas.projects.mms.mms_load_mec(trange=['2015-10-16', '2015-10-17'], probe='1')
    >>> tplot(['mms1_mec_r_gsm', 'mms1_mec_v_gsm'])


    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='mec',
            datatype=datatype, get_support_data=get_support_data, varformat=varformat, varnames=varnames, suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, notplot=notplot, 
            latest_version=latest_version, major_version=major_version, min_version=min_version, 
            cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)

    if tvars is None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_mec_set_metadata(probe, data_rate, level, suffix=suffix)

    return tvars
