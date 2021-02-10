"""
This module contains routines for loading MMS data

"""

from .mms_load_data import mms_load_data
from .fgm.mms_curl import mms_curl
from .fgm.mms_fgm_remove_flags import mms_fgm_remove_flags
from .fgm.mms_fgm_set_metadata import mms_fgm_set_metadata
from .scm.mms_scm_set_metadata import mms_scm_set_metadata
from .edp.mms_edp_set_metadata import mms_edp_set_metadata
from .dsp.mms_dsp_set_metadata import mms_dsp_set_metadata
from .edi.mms_edi_set_metadata import mms_edi_set_metadata
from .fpi.mms_fpi_set_metadata import mms_fpi_set_metadata
from .mec.mms_mec_set_metadata import mms_mec_set_metadata
from .hpca.mms_hpca_set_metadata import mms_hpca_set_metadata
from .feeps.mms_feeps_correct_energies import mms_feeps_correct_energies
from .feeps.mms_feeps_flat_field_corrections import mms_feeps_flat_field_corrections
from .feeps.mms_feeps_active_eyes import mms_feeps_active_eyes
from .feeps.mms_feeps_split_integral_ch import mms_feeps_split_integral_ch
from .feeps.mms_feeps_remove_bad_data import mms_feeps_remove_bad_data
from .feeps.mms_feeps_remove_sun import mms_feeps_remove_sun
from .feeps.mms_feeps_omni import mms_feeps_omni
from .feeps.mms_feeps_spin_avg import mms_feeps_spin_avg
from .eis.mms_eis_omni import mms_eis_omni
from .eis.mms_eis_spin_avg import mms_eis_spin_avg
from .eis.mms_eis_set_metadata import mms_eis_set_metadata
from pyspedas.mms.mec_ascii.mms_get_state_data import mms_get_state_data
from .mms_config import CONFIG

from pyspedas import tnames

import re
from pytplot import del_data
from functools import wraps

# the following decorator prints the loaded tplot variables after each load routine call
def print_vars(func):
    def wrapper(*args, **kwargs):
        variables = func(*args, **kwargs)
        if variables is None:
            return None
        if kwargs.get('available') or CONFIG['download_only']:
            print('Available files:')
        else:
            print('Loaded variables:')
        for var in variables:
            print(var)
        return variables
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

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

@print_vars
def mms_load_fgm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy',
    level='l2', instrument='fgm', datatype='', varformat=None, varnames=[], suffix='',
    keep_flagged=False, get_support_data=True, time_clip=False, no_update=False,
    available=False, notplot=False, latest_version=False, major_version=False, 
    min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    This function loads FGM data into tplot variables
    
    Parameters:
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
    
    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

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

    mms_fgm_set_metadata(probe, data_rate, level, instrument, suffix=suffix)

    return tvars

@print_vars
def mms_load_hpca(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='moments', get_support_data=None, time_clip=False, no_update=False,
    varformat=None, varnames=[], suffix='', center_measurement=False, available=False, notplot=False, 
    latest_version=False, major_version=False, min_version=None, cdf_version=None, spdf=False,
    always_prompt=False):
    """
    This function loads HPCA data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for HPCA include 'brst', 'srvy'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for HPCA are 'moments' and 'ion'; the default is 'moments'

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.

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

    if get_support_data is None:
        get_support_data = True

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='hpca',
            datatype=datatype, varformat=varformat, varnames=varnames, suffix=suffix, get_support_data=get_support_data,
            time_clip=time_clip, no_update=no_update, center_measurement=center_measurement, available=available, 
            latest_version=latest_version, major_version=major_version, min_version=min_version, cdf_version=cdf_version,
            spdf=spdf, always_prompt=always_prompt)
    
    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_hpca_set_metadata(probe=probe, suffix=suffix)
    return tvars

@print_vars
def mms_load_fpi(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast',
    level='l2', datatype=['des-moms', 'dis-moms'], varformat=None, varnames=[], suffix='',
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

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi',
            datatype=datatype, varformat=varformat, varnames=varnames, suffix=suffix, get_support_data=get_support_data,
            time_clip=time_clip, no_update=no_update, center_measurement=center_measurement, available=available, 
            notplot=notplot, latest_version=latest_version, major_version=major_version, min_version=min_version, 
            cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
    
    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_fpi_set_metadata(probe, data_rate, datatype, level, suffix=suffix)

    return tvars

@print_vars
def mms_load_scm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='', varformat=None, varnames=[], suffix='', get_support_data=False,
    time_clip=True, no_update=False, available=False, notplot=False, latest_version=False, 
    major_version=False, min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    This function loads SCM data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for SCM include ['brst' 'fast' 'slow' 'srvy']. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for SCM are: ['scsrvy', 'cal', 'scb', 'scf', 'schb', 'scm', 'scs']
            If no value is given the default is scsrvy for srvy data, and scb for brst data.

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """
    if not isinstance(data_rate, list):
        data_rate = list([data_rate])

    if isinstance(datatype, str) and datatype == '':
        # guess from data_rate
        datatype = list()
        for dr in data_rate:
            if dr == 'srvy':
                datatype.append('scsrvy')
            if dr == 'brst':
                datatype.extend(['scb', 'schb'])
        datatype = list(set(datatype)) # make it unique
    else:
        if not isinstance(datatype, list):
            datatype = list([datatype])
        # ensure datatype does not contain empty string
        datatype = list(set([dt.strip() for dt in datatype]))
        if '' in datatype:
            datatype.remove('')

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='scm',
            datatype=datatype, varformat=varformat, varnames=varnames, suffix=suffix, get_support_data=get_support_data,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, 
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, 
            always_prompt=always_prompt)

    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    coord = ''
    if level == 'l1a':
        coord = '123'
    elif level == 'l1b':
        coord = 'scm123'
    elif level == 'l2':
        coord = 'gse'

    if not isinstance(probe, list):
        probe = [probe]

    if not isinstance(datatype, list):
        datatype = [datatype]

    probe = [str(p) for p in probe]

    for p in probe:
        for dtype in datatype:
            mms_scm_set_metadata(tvars, p, dtype, coord, suffix=suffix)

    return tvars

@print_vars
def mms_load_mec(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='ephts04d', varformat=None, varnames=[], suffix='', get_support_data=False,
    time_clip=False, no_update=False, available=False, notplot=False, latest_version=False, 
    major_version=False, min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    This function loads MEC data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for MEC include ['brst', 'srvy']. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for MEC are: ['ephts04d', 'epht89q', 'epht89d']; default is 'ephts04d'

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC
            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='mec',
            datatype=datatype, get_support_data=get_support_data, varformat=varformat, varnames=varnames, suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, notplot=notplot, 
            latest_version=latest_version, major_version=major_version, min_version=min_version, 
            cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)

    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_mec_set_metadata(probe, data_rate, level, suffix=suffix)

    return tvars

@print_vars
def mms_load_feeps(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='electron', varformat=None, varnames=[], get_support_data=True, suffix='', time_clip=False,
    no_update=False, available=False, notplot=False, no_flatfield_corrections=False, data_units=['count_rate', 'intensity'], 
    latest_version=False, major_version=False, min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    This function loads FEEPS data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FEEPS include ['brst', 'srvy']. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for FEEPS are: 
                       L2, L1b: ['electron', 'ion']
                       L1a: ['electron-bottom', 'electron-top', 'ion-bottom', 'ion-top']

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='feeps',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, 
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)

    if tvars == [] or available or notplot or CONFIG['download_only']:
        return tvars

    probes = probe if isinstance(probe, list) else [probe]
    data_rates = data_rate if isinstance(data_rate, list) else [data_rate]
    levels = level if isinstance(level, list) else [level]
    datatypes = datatype if isinstance(datatype, list) else [datatype]
    data_units = data_units if isinstance(data_units, list) else [data_units]

    probes = [str(p) for p in probes]

    mms_feeps_correct_energies(probes, data_rate, level=level, suffix=suffix)

    if not no_flatfield_corrections:
        mms_feeps_flat_field_corrections(probes=probes, data_rate=data_rate, suffix=suffix)

    for probe in probes:
        for datatype in datatypes:
           mms_feeps_remove_bad_data(probe=probe, data_rate=data_rate, datatype =datatype, level=level, suffix=suffix)

           for data_unit in data_units:
               eyes = mms_feeps_active_eyes(trange, probe, data_rate, datatype, level)

               split_vars = mms_feeps_split_integral_ch(data_unit, datatype, probe, suffix=suffix, data_rate=data_rate, level=level, sensor_eyes=eyes)

               sun_removed_vars = mms_feeps_remove_sun(eyes, trange, probe=probe, datatype=datatype, data_units=data_unit, data_rate=data_rate, level=level, suffix=suffix)

               omni_vars = mms_feeps_omni(eyes, probe=probe, datatype=datatype, data_units=data_unit, data_rate=data_rate, level=level, suffix=suffix)

               tvars = tvars + split_vars + sun_removed_vars + omni_vars
               
               tvars.append(mms_feeps_spin_avg(probe=probe, data_units=data_unit, datatype=datatype, data_rate=data_rate, level=level, suffix=suffix))

    return tvars

@print_vars
def mms_load_eis(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='extof',
        varformat=None, varnames=[], get_support_data=True, suffix='', time_clip=False, no_update=False,
        available=False, notplot=False, latest_version=False, major_version=False, min_version=None, cdf_version=None, 
        spdf=False, always_prompt=False):
    """
    This function loads EIS data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for EIS include ['brst', 'srvy']. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for EIS are: ['extof', 'phxtof', and 'electronenergy']; default is 'extof'

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='epd-eis',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, prefix='', suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, 
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)

    if tvars == [] or available or notplot or CONFIG['download_only']:
        return tvars

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(datatype, list): datatype = [datatype]

    # the probes will need to be strings beyond this point
    if isinstance(probe, list):
        probe = [str(p) for p in probe]

    for probe_id in probe:
        for datatype_id in datatype:
            for data_rate_id in data_rate:
                if datatype_id == 'electronenergy':
                    e_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='electron', datatype=datatype_id, data_rate=data_rate_id, suffix=suffix)
                    # create non-spin averaged omni-directional spectra
                    e_omni_spectra = mms_eis_omni(probe_id, species='electron', data_rate=data_rate_id, datatype=datatype_id)
                    # create spin averaged omni-directional spectra
                    e_omni_spectra_spin = mms_eis_omni(probe_id, species='electron', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix+'_spin')
                    # add the vars to the output
                    if e_spin_avg_var is not None:
                        for tvar in e_spin_avg_var:
                            tvars.append(tvar)
                    if e_omni_spectra is not None:
                        tvars.append(e_omni_spectra)
                    if e_omni_spectra_spin is not None:
                        tvars.append(e_omni_spectra_spin)
                elif datatype_id == 'extof':
                    # 9Feb2021, egrimes added 'helium' species for updates coming soon to the CDFs
                    p_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='proton', datatype=datatype_id, data_rate=data_rate_id, suffix=suffix)
                    o_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='oxygen', datatype=datatype_id, data_rate=data_rate_id, suffix=suffix)
                    a_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='alpha', datatype=datatype_id, data_rate=data_rate_id, suffix=suffix)
                    h_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='helium', datatype=datatype_id, data_rate=data_rate_id, suffix=suffix)
                    # create non-spin averaged omni-directional spectra
                    p_omni_spectra = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)
                    o_omni_spectra = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)
                    a_omni_spectra = mms_eis_omni(probe_id, species='alpha', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)
                    h_omni_spectra = mms_eis_omni(probe_id, species='helium', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)
                    # create spin averaged omni-directional spectra
                    p_omni_spectra_spin = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix+'_spin')
                    o_omni_spectra_spin = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix+'_spin')
                    a_omni_spectra_spin = mms_eis_omni(probe_id, species='alpha', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix+'_spin')
                    h_omni_spectra_spin = mms_eis_omni(probe_id, species='helium', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix+'_spin')
                    # add the vars to the output
                    if p_spin_avg_var is not None:
                        for tvar in p_spin_avg_var:
                            tvars.append(tvar)
                    if o_spin_avg_var is not None:
                        for tvar in o_spin_avg_var:
                            tvars.append(tvar)
                    if a_spin_avg_var is not None:
                        for tvar in a_spin_avg_var:
                            tvars.append(tvar)
                    if h_spin_avg_var is not None:
                        for tvar in h_spin_avg_var:
                            tvars.append(tvar)
                    if p_omni_spectra is not None:
                        tvars.append(p_omni_spectra)
                    if o_omni_spectra is not None:
                        tvars.append(o_omni_spectra)
                    if a_omni_spectra is not None:
                        tvars.append(a_omni_spectra)
                    if h_omni_spectra is not None:
                        tvars.append(h_omni_spectra)
                    if p_omni_spectra_spin is not None:
                        tvars.append(p_omni_spectra_spin)
                    if o_omni_spectra_spin is not None:
                        tvars.append(o_omni_spectra_spin)
                    if a_omni_spectra_spin is not None:
                        tvars.append(a_omni_spectra_spin)
                    if h_omni_spectra_spin is not None:
                        tvars.append(h_omni_spectra_spin)
                elif datatype_id == 'phxtof':
                    # 9Feb2021, egrimes commented out oxygen calculations to match IDL updates
                    p_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='proton', datatype=datatype_id, data_rate=data_rate_id, suffix=suffix)
                    # o_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='oxygen', datatype=datatype_id, data_rate=data_rate_id, suffix=suffix)
                    # create non-spin averaged omni-directional spectra
                    p_omni_spectra = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)
                    # o_omni_spectra = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)
                    # create spin averaged omni-directional spectra
                    p_omni_spectra_spin = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix+'_spin')
                    # o_omni_spectra_spin = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, datatype=datatype_id, suffix=suffix+'_spin')
                    # add the vars to the output
                    if p_spin_avg_var is not None:
                        for tvar in p_spin_avg_var:
                            tvars.append(tvar)
                    # if o_spin_avg_var is not None:
                    #     for tvar in o_spin_avg_var:
                    #         tvars.append(tvar)
                    if p_omni_spectra is not None:
                        tvars.append(p_omni_spectra)
                    # if o_omni_spectra is not None:
                    #     tvars.append(o_omni_spectra)
                    if p_omni_spectra_spin is not None:
                        tvars.append(p_omni_spectra_spin)
                    # if o_omni_spectra_spin is not None:
                    #     tvars.append(o_omni_spectra_spin)

                mms_eis_set_metadata(tnames(tvars), data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)

    return tnames(tvars)

@print_vars
def mms_load_edi(trange=['2016-10-16', '2016-10-17'], probe='1', data_rate='srvy', level='l2', datatype='efield',
        varformat=None, varnames=[], get_support_data=False, suffix='', time_clip=False, no_update=False,
        available=False, notplot=False, latest_version=False, major_version=False, min_version=None, cdf_version=None, 
        spdf=False, always_prompt=False):
    """
    This function loads EDI data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for EDI include ['brst', 'fast', 'slow', 'srvy']. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for EDI are: ['efield', 'amb']; default is 'efield'

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='edi',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, suffix=suffix, time_clip=time_clip, 
            no_update=no_update, available=available, latest_version=latest_version, major_version=major_version, 
            min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)

    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_edi_set_metadata(probe, data_rate, level, suffix=suffix)

    return tvars

@print_vars
def mms_load_edp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype='dce',
        varformat=None, varnames=[], get_support_data=False, suffix='', time_clip=True, no_update=False,
        available=False, notplot=False, latest_version=False, major_version=False, min_version=None, cdf_version=None, 
        spdf=False, always_prompt=False):
    """
    This function loads EDP data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for EDP include ['brst', 'fast', 'slow', 'srvy']. The
            default is 'fast'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for EDP are: ['dce', 'dcv', 'ace', 'hmfe']; default is 'dce'

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='edp',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, 
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, 
            always_prompt=always_prompt)
    
    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_edp_set_metadata(probe, data_rate, level, suffix=suffix)

    return tvars

@print_vars
def mms_load_dsp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='bpsd', varformat=None, varnames=[], suffix='', get_support_data=False,
    time_clip=False, no_update=False, available=False, notplot=False, latest_version=False, 
    major_version=False, min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    This function loads DSP data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for DSP include ['fast', 'slow', 'srvy']. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for DSP are: ['epsd', 'bpsd', 'swd']; default is 'bpsd'

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='dsp',
            datatype=datatype, varformat=varformat, varnames=varnames, suffix=suffix, get_support_data=get_support_data, time_clip=time_clip, 
            no_update=no_update, available=available, latest_version=latest_version, major_version=major_version, 
            min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
    
    if tvars == None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_dsp_set_metadata(probe, data_rate, level, suffix=suffix)

    return tvars

@print_vars
def mms_load_aspoc(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='', varformat=None, varnames=[], get_support_data=False, suffix='', time_clip=False, no_update=False,
    available=False, notplot=False, latest_version=False, major_version=False, min_version=None, cdf_version=None, 
    spdf=False, always_prompt=False):
    """
    This function loads ASPOC data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for ASPOC include 'srvy', 'sitl'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for ASPOC are: ['asp1', 'asp2', 'aspoc']; default is 'aspoc'

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """

    if suffix == '':
        suffix = '_' + level
    else:
        suffix = '_' + level + suffix
    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='aspoc',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, 
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, 
            always_prompt=always_prompt)
    return tvars

@print_vars
def mms_load_fsm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='brst', 
    level='l3', datatype='8khz', get_support_data=False, time_clip=False, no_update=False, 
    available=False, varformat=None, varnames=[], notplot=False, suffix='', latest_version=False, 
    major_version=False, min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    This function loads FSM data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            the current instrument data rate for FSM is 'brst'

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatype for FSM is: 8khz

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

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed
            
        spdf: bool
            If True, download the data from the SPDF instead of the SDC

    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, notplot=notplot, varformat=varformat, probe=probe, data_rate=data_rate, 
        level=level, instrument='fsm', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip, 
        no_update=no_update, available=available, suffix=suffix, latest_version=latest_version, varnames=varnames,
        major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
    return tvars

'''
    the following wrappers allow users to import the load routines using 
    the syntax: 
    
            >>> from pyspedas.mms import fgm
            >>> fgm_data = fgm(...)

        and/or

            >>> import pyspedas
            >>> fgm_data = pyspedas.mms.fgm(...)
'''

@wraps(mms_load_state)
def state(*args, **kwargs):
    return mms_load_state(*args, **kwargs)

@wraps(mms_load_fgm)
def fgm(*args, **kwargs):
    return mms_load_fgm(*args, **kwargs)

@wraps(mms_load_scm)
def scm(*args, **kwargs):
    return mms_load_scm(*args, **kwargs)

@wraps(mms_load_fsm)
def fsm(*args, **kwargs):
    return mms_load_fsm(*args, **kwargs)

@wraps(mms_load_edp)
def edp(*args, **kwargs):
    return mms_load_edp(*args, **kwargs)

@wraps(mms_load_edi)
def edi(*args, **kwargs):
    return mms_load_edi(*args, **kwargs)

@wraps(mms_load_fpi)
def fpi(*args, **kwargs):
    return mms_load_fpi(*args, **kwargs)

@wraps(mms_load_hpca)
def hpca(*args, **kwargs):
    return mms_load_hpca(*args, **kwargs)

@wraps(mms_load_eis)
def eis(*args, **kwargs):
    return mms_load_eis(*args, **kwargs)

@wraps(mms_load_feeps)
def feeps(*args, **kwargs):
    return mms_load_feeps(*args, **kwargs)

@wraps(mms_load_aspoc)
def aspoc(*args, **kwargs):
    return mms_load_aspoc(*args, **kwargs)

@wraps(mms_load_mec)
def mec(*args, **kwargs):
    return mms_load_mec(*args, **kwargs)

@wraps(mms_load_dsp)
def dsp(*args, **kwargs):
    return mms_load_dsp(*args, **kwargs)

@wraps(mms_curl)
def curlometer(*args, **kwargs):
    return mms_curl(*args, **kwargs)
