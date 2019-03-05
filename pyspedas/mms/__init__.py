"""
This module contains routines for loading MMS data


"""

from .mms_load_data import mms_load_data
from .fgm.mms_fgm_remove_flags import mms_fgm_remove_flags
from .fgm.mms_fgm_set_metadata import mms_fgm_set_metadata
from .fpi.mms_fpi_set_metadata import mms_fpi_set_metadata

def mms_load_fgm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', instrument='fgm', datatype='', prefix='', suffix='', keep_flagged=False, get_support_data=True, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument=instrument, datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, time_clip=time_clip)
    
    if tvars == None:
        return

    # remove flagged data
    if not keep_flagged:
        mms_fgm_remove_flags(probe, data_rate, level, instrument, suffix=suffix)

    mms_fgm_set_metadata(probe, data_rate, level, instrument, suffix=suffix)
    return tvars

def mms_load_hpca(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='moments', get_support_data=False, time_clip=False):
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

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='hpca', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

def mms_load_fpi(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype=['des-moms', 'dis-moms'], prefix='', suffix='', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, time_clip=time_clip)
    
    if tvars == None:
        return

    mms_fpi_set_metadata(probe, data_rate, datatype, level, suffix=suffix)
    return tvars

def mms_load_scm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', prefix='', suffix='', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='scm', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

def mms_load_mec(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='ephts04d', prefix='', suffix='', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='mec', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

def mms_load_feeps(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='electron', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='feeps', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

def mms_load_eis(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='phxtof', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """

    from .eis.mms_eis_omni import mms_eis_omni
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='epd-eis', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip)

    if tvars == []:
        return

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(datatype, list): datatype = [datatype]

    for probe_id in probe:
        for datatype_id in datatype:
            for data_rate_id in data_rate:
                omni_spectra = mms_eis_omni(probe_id, data_rate=data_rate_id, datatype=datatype_id)
    return tvars

def mms_load_edi(trange=['2016-10-16', '2016-10-17'], probe='1', data_rate='srvy', level='l2', datatype='efield', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='edi', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

def mms_load_edp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype='dce', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='edp', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

def mms_load_dsp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='bpsd', prefix='', suffix='', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='dsp', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

def mms_load_aspoc(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', get_support_data=False, time_clip=False):
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
            
        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='aspoc', datatype=datatype, get_support_data=get_support_data, time_clip=time_clip)
    return tvars

