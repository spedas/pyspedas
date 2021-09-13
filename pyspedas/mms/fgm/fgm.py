
from pyspedas.mms.mms_load_data import mms_load_data
from pyspedas.mms.fgm.mms_fgm_remove_flags import mms_fgm_remove_flags
from pyspedas.mms.fgm.mms_fgm_set_metadata import mms_fgm_set_metadata
from pyspedas.mms.fgm.mms_split_fgm_data import mms_split_fgm_data
from pyspedas.mms.print_vars import print_vars
from pyspedas.mms.mms_config import CONFIG
from pyspedas.utilities.data_exists import data_exists

from pytplot import del_data

import re

@print_vars
def mms_load_fgm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy',
    level='l2', instrument='fgm', datatype='', varformat=None, varnames=[], suffix='',
    keep_flagged=False, get_support_data=True, time_clip=False, no_update=False,
    available=False, notplot=False, latest_version=False, major_version=False, 
    min_version=None, cdf_version=None, spdf=False, always_prompt=False, no_split_vars=False,
    get_fgm_ephemeris=False):
    """
    This function loads FGM data into tplot variables
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FGM include 'brst' 'fast' 'slow' 'srvy'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            no datatype for FGM instrument (all science data are loaded)

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

        keep_flagged: bool
            If True, don't remove flagged data (flagged data are set to NaNs by
            default, this keyword turns this off)

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

        get_fgm_ephemeris: bool
            Keep the ephemeris variables in the FGM files
            
    Returns:
        List of tplot variables created.

    """

    if (varformat is not None) and (not keep_flagged) and (not available) and (not notplot):
        varformat_fetch = varformat+'|*_flag_*'
    else:
        varformat_fetch = varformat

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument=instrument,
            datatype=datatype, varformat=varformat_fetch, varnames=varnames, suffix=suffix, get_support_data=get_support_data,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, major_version=major_version, 
            min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
    
    if tvars is None or available or notplot or CONFIG['download_only']:
        return tvars

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]

    # the probes will need to be strings beyond this point
    if isinstance(probe, list):
        probe = [str(p) for p in probe]

    # remove flagged data
    if not keep_flagged:
        mms_fgm_remove_flags(probe, data_rate, level, instrument, suffix=suffix)
        # Delete the flags variable if it was not originally requested
        if varformat is not None:
            regex = re.compile(varformat.replace("*", ".*"))
            tvars_to_delete = [tvar for tvar in tvars if not re.match(regex, tvar)]
            for tvar in tvars_to_delete:
                del_data(tvar)
                tvars.remove(tvar)

    for prb in probe:
        for drate in data_rate:
            for lvl in level:
                if not no_split_vars:
                    out = mms_split_fgm_data(prb, drate, lvl, instrument, suffix=suffix)
                    tvars.extend(out)

                if lvl.lower() != 'ql':
                    # delete the ephemeris variables if not requested
                    if not get_fgm_ephemeris:
                        if data_exists('mms'+prb+'_'+instrument+'_r_gse_'+drate+'_'+lvl+suffix):
                            del_data('mms'+prb+'_'+instrument+'_r_gse_'+drate+'_'+lvl+suffix)
                            tvars.remove('mms'+prb+'_'+instrument+'_r_gse_'+drate+'_'+lvl+suffix)
                        if data_exists('mms'+prb+'_'+instrument+'_r_gsm_'+drate+'_'+lvl+suffix):
                            del_data('mms'+prb+'_'+instrument+'_r_gsm_'+drate+'_'+lvl+suffix)
                            tvars.remove('mms'+prb+'_'+instrument+'_r_gsm_'+drate+'_'+lvl+suffix)
                        if data_exists('mms'+prb+'_pos_gse'+suffix):
                            del_data('mms'+prb+'_pos_gse'+suffix)
                            tvars.remove('mms'+prb+'_pos_gse'+suffix)
                        if data_exists('mms'+prb+'_pos_gsm'+suffix):
                            del_data('mms'+prb+'_pos_gsm'+suffix)
                            tvars.remove('mms'+prb+'_pos_gsm'+suffix)

    mms_fgm_set_metadata(probe, data_rate, level, instrument, suffix=suffix)

    return tvars
