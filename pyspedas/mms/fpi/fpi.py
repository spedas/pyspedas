
from pyspedas.mms.mms_load_data import mms_load_data
from pyspedas.mms.fpi.mms_fpi_set_metadata import mms_fpi_set_metadata
from pyspedas.mms.fpi.mms_load_fpi_calc_pad import mms_load_fpi_calc_pad
from pyspedas.mms.print_vars import print_vars
from pyspedas.mms.mms_config import CONFIG

@print_vars
def mms_load_fpi(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast',
    level='l2', datatype='*', varformat=None, varnames=[], suffix='',
    get_support_data=False, time_clip=False, no_update=False, center_measurement=False,
    available=False, notplot=False, latest_version=False, major_version=False, 
    min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    This function loads FPI data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FPI include 'brst', 'fast'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for FPI are:
             'des-moms', 'dis-moms' (default)
             'des-dist', 'dis-dist'

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        center_measurement: bool
            If True, the CDF epoch variables are time-shifted to the middle
            of the accumulation interval by their DELTA_PLUS_VAR and
            DELTA_MINUS_VAR variable attributes

        notplot: bool
            If True, then data are returned in a hash table instead of 
            being stored in tplot variables (useful for debugging, and
            access to multi-dimensional data products)

        available: bool
            If True, simply return the available data files (without downloading)
            for the requested paramters

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten

        cdf_version: str
            Specify a specific CDF version # to load (e.g., cdf_version='4.3.0')

        min_version: str
            Specify a minimum CDF version # to load

        latest_version: bool
            Only grab the latest CDF version in the requested time interval

        major_version: bool
            Only open the latest major CDF version (e.g., X in vX.Y.Z) in the requested time interval

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC
            
    Returns:
        List of tplot variables created.

    """

    # different datatypes for burst mode files
    if data_rate.lower() == 'brst':
        if isinstance(datatype, str):
            if (datatype == '*' or datatype == '') and level.lower() != 'ql':
                datatype = ['des-dist', 'dis-dist', 'dis-moms', 'des-moms']
    else:
        if isinstance(datatype, str):
            if (datatype == '*' or datatype == '') and level.lower() == 'ql':
                datatype = ['des', 'dis']
            if (datatype == '*' or datatype == '') and level.lower() != 'ql':
                datatype = ['des-dist', 'dis-dist', 'dis-moms', 'des-moms']

    # kludge for level = 'sitl' -> datatype shouldn't be defined for sitl data.
    if level.lower() == 'sitl' or level.lower() == 'trig':
        datatype = ''

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi',
            datatype=datatype, varformat=varformat, varnames=varnames, suffix=suffix, get_support_data=get_support_data,
            time_clip=time_clip, no_update=no_update, center_measurement=center_measurement, available=available, 
            notplot=notplot, latest_version=latest_version, major_version=major_version, min_version=min_version, 
            cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
    
    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_fpi_set_metadata(probe, data_rate, datatype, level, suffix=suffix)

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(datatype, list): datatype = [datatype]
    if not isinstance(level, list): level = [level]

    for prb in probe:
        for drate in data_rate:
            for dtype in datatype:
                for lvl in level:
                    out_var = mms_load_fpi_calc_pad(probe=prb, level=lvl, datatype=dtype, data_rate=drate, suffix=suffix, autoscale=True)
                    if out_var:
                        tvars.extend(out_var)

    return tvars
